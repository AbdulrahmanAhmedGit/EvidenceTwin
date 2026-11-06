"""Explicit migrations restricted to disposable local test databases in this increment."""
import os
from alembic import context
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

url=os.environ.get('ET_EXECUTION_TEST_ADMIN_DSN')
if not url: raise RuntimeError('Explicit disposable test DSN required')
u=make_url(url)
import re
if u.drivername!='postgresql+psycopg' or not re.fullmatch(r'et_test_[a-f0-9]+',u.database or ''):
    raise RuntimeError('Refusing non-disposable migration target')
destination=u.query.get('host',u.host)
if destination not in {'127.0.0.1','localhost'} and not (destination and destination.startswith('/tmp/et_pg_')):
    raise RuntimeError('Only local isolated PostgreSQL is authorized')
if context.is_offline_mode(): raise RuntimeError('Offline mode disabled for this restricted test migration')
engine=create_engine(u,hide_parameters=True)
try:
    with engine.connect() as connection:
        if connection.execute(text('select current_database()')).scalar_one()!=u.database:
            raise RuntimeError('Database identity mismatch')
        connection.rollback()
        context.configure(connection=connection,version_table_schema="public")
        with context.begin_transaction(): context.run_migrations()
finally: engine.dispose()
