import pytest
from sqlalchemy import inspect,text,insert,select
from sqlalchemy.exc import DBAPIError,IntegrityError
from alembic import command
from alembic.config import Config
from pathlib import Path
from evidencetwin_backend.execution import tables as t

def test_ex01_metadata_and_upgrade_replay(pg):
    i=inspect(pg.admin)
    assert set(i.get_table_names(schema='et_execution'))=={x.name for x in t.metadata.tables.values()}
    assert len(t.metadata.tables)==16
    for table in t.metadata.tables.values():
        cols={x['name']:str(x['type']) for x in i.get_columns(table.name,schema='et_execution')}
        assert cols=={x.name:str(x.type) for x in table.columns}
    command.upgrade(Config(str(Path(__file__).resolve().parents[2]/'alembic.ini')),'head')

def test_ex02_invalid_capacity_rolls_back(pg):
    with pytest.raises(IntegrityError):
        with pg.admin.begin() as c:c.execute(insert(t.capacity_scopes).values(key='invalid',kind='analyses',capacity=1,in_use=2,version=1))

def test_ex43_runtime_cannot_ddl(pg):
    with pytest.raises(DBAPIError):
        with pg.db.engine.begin() as c:c.execute(text('CREATE TABLE et_execution.forbidden(id int)'))
    with pytest.raises(DBAPIError):
        with pg.db.engine.begin() as c:c.execute(text('TRUNCATE et_execution.jobs'))

def test_ex01_downgrade_upgrade_only_disposable(pg):
    cfg=Config(str(Path(__file__).resolve().parents[2]/'alembic.ini'))
    command.downgrade(cfg,'base');command.upgrade(cfg,'head')
    assert len(inspect(pg.admin).get_table_names(schema='et_execution'))==16

def test_ex03_cross_job_attempt_fk_and_ex04_unique_executable(pg):
    from uuid import uuid4
    a=pg.repo.submit(pg.p,pg.snapshot,'a');b=pg.repo.submit(pg.p,pg.snapshot,'b')
    from sqlalchemy import update,func
    with pg.admin.connect() as c:attempt=c.execute(select(t.jobs.c.current_attempt_id).where(t.jobs.c.id==b)).scalar_one()
    with pytest.raises(IntegrityError):
        with pg.admin.begin() as c:c.execute(update(t.jobs).where(t.jobs.c.id==a).values(current_attempt_id=attempt))
    with pytest.raises(IntegrityError):
        with pg.admin.begin() as c:c.execute(insert(t.attempts).values(id=uuid4(),job_id=a,ordinal=2,state='pending',version=1,created_at=func.clock_timestamp()))

def test_ex46_disposable_backup_restore_manifest_identity(pg,tmp_path):
    import subprocess,os
    from uuid import uuid4
    from sqlalchemy import create_engine
    from helpers import PAYLOAD
    job=pg.repo.submit(pg.p,pg.snapshot,'s')
    url=pg.admin_url;environment=dict(os.environ,PGHOST=url.query['host'],PGPORT=url.query['port'],PGUSER=url.username)
    if url.password:environment['PGPASSWORD']=url.password
    dump=tmp_path/'execution.dump'
    subprocess.run(['/usr/lib/postgresql/18/bin/pg_dump','-Fc','--no-owner','--no-privileges','-f',str(dump),pg.name],env=environment,check=True,capture_output=True)
    name='et_test_'+uuid4().hex
    admin=create_engine(url.set(database='postgres'),isolation_level='AUTOCOMMIT')
    try:
        with admin.connect() as c:c.execute(text('CREATE DATABASE '+name))
        subprocess.run(['/usr/lib/postgresql/18/bin/pg_restore','--no-owner','--no-privileges','--exit-on-error','-d',name,str(dump)],env=environment,check=True,capture_output=True)
        restored=create_engine(url.set(database=name))
        try:
            with restored.connect() as a,pg.admin.connect() as b:
                assert a.execute(select(t.snapshots.c.manifest_sha256)).scalar_one()==b.execute(select(t.snapshots.c.manifest_sha256)).scalar_one()
                assert a.execute(select(t.jobs.c.owner_ref).where(t.jobs.c.id==job)).scalar_one()=='alice'
        finally:restored.dispose()
    finally:
        with admin.connect() as c:c.execute(text('DROP DATABASE '+name))
        admin.dispose()

def test_ex01_constraints_and_indexes_match_static_metadata(pg):
    i=inspect(pg.admin)
    for table in t.metadata.tables.values():
        assert i.get_pk_constraint(table.name,schema='et_execution')['constrained_columns']==[c.name for c in table.primary_key]
        assert {x['name'] for x in i.get_foreign_keys(table.name,schema='et_execution')}=={x.name for x in table.foreign_key_constraints}
        assert {x['name'] for x in i.get_check_constraints(table.name,schema='et_execution')}=={x.name for x in table.constraints if x.__class__.__name__=='CheckConstraint'}
        indexes={x['name'] for x in i.get_indexes(table.name,schema='et_execution') if not x.get('duplicates_constraint')}
        assert indexes=={x.name for x in table.indexes}

def test_ex02_09_bad_states_and_cross_state_candidates_reject(pg):
    from sqlalchemy import update
    from evidencetwin_backend.execution.contracts import Rejected
    job=pg.repo.submit(pg.p,pg.snapshot,'s')
    for values in [{'state':'invented'},{'version':0},{'attempt_count':4},{'state':'succeeded'}]:
        with pytest.raises(IntegrityError):
            with pg.admin.begin() as c:c.execute(update(t.jobs).where(t.jobs.c.id==job).values(**values))
    with pytest.raises(Rejected):
        with pg.admin.begin() as c:
            c.execute(update(t.jobs).where(t.jobs.c.id==job).values(state='running'))
            pg.repo._pair(c,job)
