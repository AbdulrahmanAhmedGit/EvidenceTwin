"""Disposable PostgreSQL fixtures, isolated from application .env/instance data."""
import os
import secrets
from pathlib import Path
import re
import sys
from uuid import uuid4
from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine,text,insert
from sqlalchemy.engine import make_url
from alembic.config import Config
from alembic import command
sys.path.insert(0,str(Path(__file__).parent))
from helpers import adapters,principal,seed_snapshot
from evidencetwin_backend.execution.database import Database
from evidencetwin_backend.execution.repository import Repository
from evidencetwin_backend.execution import tables as t

pytestmark=pytest.mark.execution_postgres

@pytest.fixture
def pg(monkeypatch):
    dsn=os.getenv('ET_EXECUTION_TEST_CLUSTER_DSN')
    if not dsn:pytest.fail('Explicit ET_EXECUTION_TEST_CLUSTER_DSN required for PostgreSQL acceptance')
    u=make_url(dsn);host=u.query.get('host',u.host)
    if u.drivername!='postgresql+psycopg' or u.database!='postgres':
        pytest.fail('Explicit disposable cluster administrator DSN required')
    unix=host and host.startswith('/tmp/et_pg_')
    if unix:
        root=Path(host).parent
        if not (root/'data/PG_VERSION').exists() or root.stat().st_uid!=os.getuid() or root.stat().st_mode&0o077:
            pytest.fail('Disposable cluster ownership/sentinel check failed')
    elif not (host in {'localhost','127.0.0.1'} and u.port not in {None,5432} and u.username=='et_test_admin'
              and os.getenv('ET_EXECUTION_TEST_DISPOSABLE')=='1'):
        pytest.fail('Refusing non-disposable test server')
    admin=create_engine(u,isolation_level='AUTOCOMMIT',hide_parameters=True)
    name='et_test_'+uuid4().hex;role='et_runtime_'+uuid4().hex
    password=secrets.token_urlsafe(24)
    with admin.connect() as c:
        assert c.execute(text('SHOW server_version')).scalar_one().startswith('18.6')
        if not unix:
            assert c.execute(text("SELECT current_setting('et_execution.test_cluster',true)")).scalar_one()=='enabled'
        # Identifiers are strictly generated, never caller supplied. Use dialect identifier quoting.
        q=c.dialect.identifier_preparer.quote_identifier
        c.execute(text('CREATE DATABASE '+q(name)))
        c.execute(text('CREATE ROLE '+q(role)+' LOGIN'))
        # Bind values; server-side format quotes identifiers/literals without embedding secrets in statements.
        c.execute(text("SELECT set_config('et_test.role',:role,false),set_config('et_test.password',:password,false)"),{'role':role,'password':password})
        c.execute(text("DO $$ BEGIN EXECUTE format('ALTER ROLE %I PASSWORD %L',current_setting('et_test.role'),current_setting('et_test.password')); END $$"))
    target=u.set(database=name)
    monkeypatch.setenv('ET_EXECUTION_TEST_ADMIN_DSN',target.render_as_string(hide_password=False))
    command.upgrade(Config(str(Path(__file__).resolve().parents[2]/'alembic.ini')),'head')
    owner=create_engine(target,hide_parameters=True)
    try:
        with owner.begin() as c:
            q=c.dialect.identifier_preparer.quote_identifier
            c.execute(text('GRANT CONNECT ON DATABASE '+q(name)+' TO '+q(role)))
            c.execute(text('GRANT USAGE ON SCHEMA et_execution TO '+q(role)))
            c.execute(text('GRANT SELECT ON ALL TABLES IN SCHEMA et_execution TO '+q(role)))
            writable=[x for x in t.metadata.tables.values() if x.name not in {'guards','snapshots','artifacts'}]
            for table in writable:c.execute(text('GRANT INSERT,UPDATE ON et_execution.'+q(table.name)+' TO '+q(role)))
            c.execute(text('GRANT UPDATE(version) ON et_execution.guards TO '+q(role)))
            c.execute(text('GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA et_execution TO '+q(role)))
            for key,kind,limit in [('analyses','analyses',2),('global_llm','global_llm',2),('provider:test-provider-config','provider_llm',2)]:
                c.execute(insert(t.capacity_scopes).values(key=key,kind=kind,capacity=limit,in_use=0,version=1))
            sid=seed_snapshot(c)
        worker_url=target.set(username=role,password=password)
        db=Database(worker_url)
        a=adapters();repo=Repository(db,a)
        yield SimpleNamespace(admin=owner,admin_url=target,url=worker_url,db=db,repo=repo,adapters=a,p=principal(),snapshot=sid,name=name,role=role)
    finally:
        if 'db' in locals():db.close()
        owner.dispose()
        with admin.connect() as c:
            c.execute(text('SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=:name AND pid<>pg_backend_pid()'),{'name':name})
            if not re.fullmatch('et_test_[a-f0-9]{32}',name):raise RuntimeError('Unsafe cleanup')
            q=c.dialect.identifier_preparer.quote_identifier
            c.execute(text('DROP DATABASE '+q(name)))
            c.execute(text('DROP ROLE '+q(role)))
        admin.dispose()
