from uuid import uuid4
import pytest
from sqlalchemy import select,func
from helpers import PAYLOAD
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.recovery import Recovery
from evidencetwin_backend.execution.contracts import Rejected

def test_ex15_steps_survive_retry_and_explicit_reuse(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    pg.repo.publish(pg.p,lease,'step',PAYLOAD,step='fixture-check')
    with pg.admin.connect() as c:original=c.execute(select(t.steps.c.id)).scalar_one()
    Recovery(pg.repo,lambda a,b:0).retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,retryable=True,proof=pg.adapters.stop.proof(lease),reason='transient_preacceptance')
    new=pg.repo.claim(pg.p,uuid4());pg.repo.publish(pg.p,new,'reuse',PAYLOAD,step='fixture-check',reused_from=original)
    with pg.admin.connect() as c:
        assert c.execute(select(func.count()).select_from(t.steps)).scalar_one()==2
        assert c.execute(select(t.steps.c.reused_from).where(t.steps.c.attempt_id==new.attempt_id)).scalar_one()==original

def test_ex22_pending_cancellation_idempotent(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');assert pg.repo.cancel(pg.p,job,'c',expected_version=1)=='cancelled'
    assert pg.repo.cancel(pg.p,job,'c',expected_version=1)=='cancelled'
    assert pg.repo.claim(pg.p,uuid4()) is None

def test_ex23_running_cancellation_finalize_without_worker_ack(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    assert pg.repo.cancel(pg.p,job,'c',expected_version=lease.job_version)=='cancellation_requested'
    j=pg.repo.get(pg.p,job)
    assert Recovery(pg.repo).finalize_cancel(pg.p,job,'finish',expected_version=j['version'])=='cancelled'
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'late',PAYLOAD)
    with pg.admin.connect() as c:assert c.execute(select(t.capacity_scopes.c.in_use).where(t.capacity_scopes.c.key=='analyses')).scalar_one()==1

def test_ex18_19_scheduling_stop_keeps_attempt_history(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s')
    assert Recovery(pg.repo).scheduling_stop(pg.p,job,'stop',expected_version=1)=='failed'
    with pg.admin.connect() as c:assert c.execute(select(t.attempts.c.state)).scalar_one()=='cancelled'

def test_ex22_actual_pending_claim_cancellation_race(pg):
    import multiprocessing as mp
    from helpers import pending_race_process
    job=pg.repo.submit(pg.p,pg.snapshot,'s');ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    workers=[ctx.Process(target=pending_race_process,args=(pg.url.render_as_string(hide_password=False),str(job),kind,start,out)) for kind in ['claim','cancel']]
    for w in workers:w.start()
    start.set();results=[out.get(timeout=15) for _ in workers]
    for w in workers:w.join(10);assert w.exitcode==0
    assert not any(x[0]=='error' for x in results),results
    state=pg.repo.get(pg.p,job)['state']
    if state=='running':assert ('claim',True) in results and ('rejected','stale_revision') in results
    else:assert state=='cancelled' and ('claim',False) in results and ('cancel','cancelled') in results
