import multiprocessing as mp
from uuid import uuid4
import pytest
from sqlalchemy import select,func,update
from helpers import claim_process,seed_snapshot,principal
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.contracts import Conflict,CapacityUnavailable

def test_ex06_07_submission_idempotency(pg):
    j=pg.repo.submit(pg.p,pg.snapshot,'key');assert pg.repo.submit(pg.p,pg.snapshot,'key')==j
    with pg.admin.begin() as c:
        # Same case identity, changed snapshot is a conflicting submission.
        sid=seed_snapshot(c);case=c.execute(select(t.snapshots.c.case_ref).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
        from helpers import canonical,digest
        import json
        body=json.loads(bytes(c.execute(select(t.snapshots.c.manifest).where(t.snapshots.c.id==sid)).scalar_one()))
        body['case_ref']=case;encoded=canonical(body)
        c.execute(update(t.snapshots).where(t.snapshots.c.id==sid).values(case_ref=case,manifest=encoded,manifest_sha256=digest(encoded)))
    with pytest.raises(Conflict):pg.repo.submit(pg.p,sid,'key')
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.jobs)).scalar_one()==1

def test_ex10_concurrent_claims_two_processes(pg):
    j=pg.repo.submit(pg.p,pg.snapshot,'submit');ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    workers=[ctx.Process(target=claim_process,args=(pg.url.render_as_string(hide_password=False),'alice',start,out)) for _ in range(2)]
    for w in workers:w.start()
    start.set();results=[out.get(timeout=15) for _ in workers]
    for w in workers:w.join(10);assert w.exitcode==0
    assert all(x[0]=='ok' for x in results),results
    assert sum(x[1] is not None for x in results)==1
    assert pg.repo.get(pg.p,j)['state']=='running'

def test_ex11_third_job_stays_queued(pg):
    jobs=[pg.repo.submit(pg.p,pg.snapshot,str(i)) for i in range(3)]
    assert pg.repo.claim(pg.p,uuid4());assert pg.repo.claim(pg.p,uuid4())
    with pytest.raises(CapacityUnavailable):pg.repo.claim(pg.p,uuid4())
    assert pg.repo.get(pg.p,jobs[2])['state']=='queued'

def test_ex13_admission_bound(pg):
    for i in range(4):pg.repo.submit(pg.p,pg.snapshot,str(i))
    with pytest.raises(CapacityUnavailable):pg.repo.submit(pg.p,pg.snapshot,'fifth')

def test_ex12_fair_accounts(pg):
    a=[pg.repo.submit(pg.p,pg.snapshot,str(i)) for i in range(2)]
    bob=principal('bob')
    with pg.admin.begin() as c:sid=seed_snapshot(c,bob)
    b=pg.repo.submit(bob,sid,'bob')
    dispatcher=principal('scheduler')
    from evidencetwin_backend.execution.contracts import Principal
    dispatcher=Principal('scheduler','fixture-dispatcher',frozenset({'dispatcher'}))
    first=pg.repo.claim(dispatcher,uuid4());second=pg.repo.claim(dispatcher,uuid4())
    assert {first.job_id,second.job_id}=={a[0],b}

def test_ex05_fault_after_queue_insert_rolls_back_everything(pg,monkeypatch):
    def fail(*args):raise RuntimeError('fixture injected before commit')
    monkeypatch.setattr(pg.repo,'_pair',fail)
    with pytest.raises(RuntimeError):pg.repo.submit(pg.p,pg.snapshot,'fault')
    with pg.admin.connect() as c:
        for table in (t.jobs,t.attempts,t.queue_entries,t.operations):assert c.execute(select(func.count()).select_from(table)).scalar_one()==0

def test_ex12_locked_fifo_head_not_overtaken(pg):
    from helpers import lock_queue_process
    first=pg.repo.submit(pg.p,pg.snapshot,'first');pg.repo.submit(pg.p,pg.snapshot,'second')
    ctx=mp.get_context('spawn');ready=ctx.Event();release=ctx.Event()
    process=ctx.Process(target=lock_queue_process,args=(pg.url.render_as_string(hide_password=False),str(first),ready,release))
    process.start()
    try:
        assert ready.wait(10)
        assert pg.repo.claim(pg.p,uuid4()) is None
    finally:release.set();process.join(10)
    assert process.exitcode==0
    assert pg.repo.claim(pg.p,uuid4()).job_id==first
