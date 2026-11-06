from dataclasses import replace
import time
from uuid import uuid4
import pytest
from sqlalchemy import text,select,update,func
from evidencetwin_backend.execution.contracts import Contention,CommitUnknown,Rejected
from evidencetwin_backend.execution.database import Database
from evidencetwin_backend.execution import tables as t

def test_ex28_statement_timeout_is_bounded(pg):
    started=time.monotonic()
    with pytest.raises(Contention):pg.db.run(lambda c:c.execute(text('SELECT pg_sleep(3)')))
    assert time.monotonic()-started<2.5

def test_ex27_actual_connection_loss_is_indeterminate(pg):
    def lost(c):
        pid=c.execute(text('SELECT pg_backend_pid()')).scalar_one()
        with pg.admin.begin() as other:other.execute(text('SELECT pg_terminate_backend(:pid)'),{'pid':pid})
        c.execute(text('SELECT 1'))
    with pytest.raises(CommitUnknown):pg.db.run(lost)

def test_ex17_expired_lease_cannot_publish(pg):
    from datetime import timedelta
    from helpers import PAYLOAD
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pg.admin.begin() as c:c.execute(update(t.attempts).where(t.attempts.c.id==lease.attempt_id).values(lease_until=func.clock_timestamp()-timedelta(seconds=1)))
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'p',PAYLOAD)

def test_ex45_core_only_default_isolation(pg):
    assert pg.db.run(lambda c:c.execute(text('SHOW transaction_isolation')).scalar_one())=='read committed'
    assert pg.db.run(lambda c:c.execute(text('SHOW lock_timeout')).scalar_one())=='500ms'

def test_ex26_real_deadlock_retries_database_only(pg):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from evidencetwin_backend.execution.database import Database
    barrier=threading.Barrier(2);calls=[0,0]
    def run(index):
        db=Database(pg.admin_url)
        keys=['admission','dispatch'] if index==0 else ['dispatch','admission']
        def transaction(c):
            calls[index]+=1
            c.execute(text("SELECT set_config('deadlock_timeout','20ms',true)"))
            c.execute(select(t.control).where(t.control.c.key==keys[0]).with_for_update())
            if calls[index]==1:barrier.wait(timeout=3)
            c.execute(select(t.control).where(t.control.c.key==keys[1]).with_for_update())
            for key in keys:c.execute(update(t.control).where(t.control.c.key==key).values(sequence=t.control.c.sequence+1))
        try:db.run(transaction)
        finally:db.close()
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,[0,1]))
    assert sorted(calls)==[1,2]
    with pg.admin.connect() as c:assert [x[0] for x in c.execute(select(t.control.c.sequence))]==[2,2]

def test_ex42_rejection_audit_failure_never_claims_durable_success(pg,monkeypatch):
    from helpers import PAYLOAD
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    def unavailable(*args,**kwargs):raise RuntimeError('fixture audit unavailable')
    monkeypatch.setattr(pg.repo,'_audit',unavailable)
    from dataclasses import replace
    with pytest.raises(Rejected) as info:pg.repo.publish(pg.p,replace(lease,fence=lease.fence+1),'stale',PAYLOAD)
    assert info.value.audit_recorded is False
    assert pg.repo.get(pg.p,job)['state']=='running'

def test_ex26_retry_exhaustion_rolls_back_without_new_scientific_attempt(pg):
    calls=[]
    def transient(c):
        calls.append(1)
        c.execute(update(t.control).where(t.control.c.key=='admission').values(sequence=t.control.c.sequence+1))
        c.execute(text("DO $$ BEGIN RAISE EXCEPTION 'fixture transient' USING ERRCODE='40P01'; END $$"))
    with pytest.raises(Contention):pg.db.run(transient)
    assert len(calls)==3
    with pg.admin.connect() as c:assert c.execute(select(t.control.c.sequence).where(t.control.c.key=='admission')).scalar_one()==0

def test_ex28_pool_checkout_timeout(pg):
    a=pg.db.engine.connect();b=pg.db.engine.connect();started=time.monotonic()
    try:
        with pytest.raises(Contention,match='pool_timeout'):pg.db.run(lambda c:None)
        assert time.monotonic()-started<2
    finally:a.close();b.close()

def test_ex17_time_sample_after_lock_wait(pg):
    import multiprocessing as mp
    import threading
    from datetime import timedelta
    from helpers import lock_queue_process,PAYLOAD
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    ctx=mp.get_context('spawn');ready=ctx.Event();release=ctx.Event()
    child=ctx.Process(target=lock_queue_process,args=(pg.url.render_as_string(hide_password=False),str(job),ready,release));child.start()
    try:
        assert ready.wait(10)
        with pg.admin.begin() as c:c.execute(update(t.attempts).where(t.attempts.c.id==lease.attempt_id).values(lease_until=func.clock_timestamp()+timedelta(seconds=.05)))
        timer=threading.Timer(.2,release.set);timer.start()
        with pytest.raises(Rejected,match='stale_execution'):pg.repo.publish(pg.p,lease,'blocked',PAYLOAD)
        timer.join()
    finally:release.set();child.join(10)
    assert child.exitcode==0
