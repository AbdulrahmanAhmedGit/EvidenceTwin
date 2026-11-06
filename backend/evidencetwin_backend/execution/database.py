"""Short Core-only transactions with explicit rollback and uncertainty semantics."""
import random
import time
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError, TimeoutError as PoolTimeout
from .contracts import CommitUnknown, Contention, Conflict, IntegrationUnavailable, Rejected
from .settings import Settings

class Database:
    def __init__(self, url, settings=None):
        self.settings=settings or Settings()
        u=make_url(url)
        if u.drivername!='postgresql+psycopg': raise ValueError('Psycopg 3 PostgreSQL URL required')
        destination=u.query.get('host',u.host)
        if destination not in {'localhost','127.0.0.1','::1'} and not (destination and destination.startswith('/tmp/et_pg_')):
            if u.query.get('sslmode')!='verify-full': raise ValueError('Remote PostgreSQL requires verify-full TLS')
        self.engine=create_engine(u,isolation_level='READ COMMITTED',pool_size=2,max_overflow=0,
            pool_timeout=self.settings.pool_timeout,hide_parameters=True,
            connect_args={'connect_timeout':2,'tcp_user_timeout':2000})

    def run(self, callback, *, heartbeat=False):
        start=time.monotonic()
        limit=1 if heartbeat else self.settings.db_attempts
        for n in range(limit):
            try:
                with self.engine.connect() as conn:
                    with conn.begin():
                        conn.execute(text("SELECT set_config('lock_timeout',:v,true)"),{'v':f'{self.settings.lock_timeout_ms}ms'})
                        conn.execute(text("SELECT set_config('statement_timeout',:v,true)"),{'v':f'{self.settings.statement_timeout_ms}ms'})
                        conn.execute(text("SELECT set_config('idle_in_transaction_session_timeout','2000ms',true)"))
                        result=callback(conn)
                        if time.monotonic()-start>self.settings.db_deadline:
                            raise Contention('transaction_deadline')
                    return result
            except PoolTimeout:
                raise Contention('pool_timeout') from None
            except DBAPIError as exc:
                code=getattr(exc.orig,'sqlstate',None)
                if code in {'40P01','40001'} and n+1<limit and time.monotonic()-start<self.settings.db_deadline:
                    time.sleep(random.uniform(0,min(.2,.05*2**n)))
                    continue
                if exc.connection_invalidated or (code and code.startswith('08')):
                    raise CommitUnknown('commit_outcome_unknown') from None
                if code in {'40P01','40001','55P03','57014'}:
                    raise Contention('database_contention') from None
                if code=='23505':raise Conflict('integrity_conflict') from None
                if code and code.startswith('42'):raise IntegrationUnavailable('schema_incompatible') from None
                raise Rejected('database_contract_error') from None
        raise Contention('database_retry_exhausted')

    def close(self): self.engine.dispose()
