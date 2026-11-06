from uuid import uuid4
from datetime import timedelta
from dataclasses import replace
import pytest
from sqlalchemy import select,update,func
from helpers import PAYLOAD,slow_task
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.recovery import Recovery
from evidencetwin_backend.execution.supervisor import Supervisor
from evidencetwin_backend.execution.contracts import Rejected

def test_ex16_18_heartbeat_and_lost_ack_replay(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    new=pg.repo.heartbeat(pg.p,lease,'heartbeat')
    assert new.attempt_version==lease.attempt_version+1
    with pg.admin.connect() as c:expiry=c.execute(select(t.attempts.c.lease_until).where(t.attempts.c.id==lease.attempt_id)).scalar_one()
    assert pg.repo.heartbeat(pg.p,lease,'heartbeat')==new
    with pg.admin.connect() as c:assert c.execute(select(t.attempts.c.lease_until).where(t.attempts.c.id==lease.attempt_id)).scalar_one()==expiry
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'old',PAYLOAD)

def test_ex14_16_20_real_child_stop_recovery(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    supervisor=Supervisor(replace(pg.repo.settings,stop_grace=.03,kill_grace=.5))
    pg.repo.adapters=replace(pg.adapters,stop=supervisor)
    handle=supervisor.start(lease.owner_instance,slow_task)
    proof=supervisor.stop(handle)
    assert not handle.process.is_alive()
    with pg.admin.begin() as c:c.execute(update(t.attempts).where(t.attempts.c.id==lease.attempt_id).values(lease_until=func.clock_timestamp()-timedelta(seconds=1)))
    recovery=Recovery(pg.repo,lambda a,b:0)
    assert recovery.retire(pg.p,lease.job_id,'recover',expected_version=lease.job_version,expected_attempt_id=lease.attempt_id,expected_fence=lease.fence,retryable=True,proof=proof)=='retry_wait'
    new=pg.repo.claim(pg.p,uuid4());assert new.fence>lease.fence and new.attempt_id!=lease.attempt_id
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'late-success',PAYLOAD)
    with pytest.raises(Rejected):recovery.retire(pg.p,lease.job_id,'late-failure',expected_version=lease.job_version,lease=lease)

def test_ex14_recovery_requires_expiry_and_stop_proof(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());r=Recovery(pg.repo,lambda a,b:0)
    with pytest.raises(Rejected):r.retire(pg.p,lease.job_id,'too-early',expected_version=lease.job_version,expected_attempt_id=lease.attempt_id,expected_fence=lease.fence,retryable=True)
    with pg.admin.begin() as c:c.execute(update(t.attempts).where(t.attempts.c.id==lease.attempt_id).values(lease_until=func.clock_timestamp()-timedelta(seconds=1)))
    r.retire(pg.p,lease.job_id,'expired',expected_version=lease.job_version,expected_attempt_id=lease.attempt_id,expected_fence=lease.fence,retryable=True)
    assert pg.repo.claim(pg.p,uuid4()) is None
    r.release_stopped(pg.p,lease.job_id,pg.adapters.stop.proof(lease))
    assert pg.repo.claim(pg.p,uuid4())

def test_ex24_two_recovery_processes_one_replacement(pg):
    import multiprocessing as mp
    from helpers import recovery_process
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pg.admin.begin() as c:c.execute(update(t.attempts).where(t.attempts.c.id==lease.attempt_id).values(lease_until=func.clock_timestamp()-timedelta(seconds=1)))
    ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    workers=[ctx.Process(target=recovery_process,args=(pg.url.render_as_string(hide_password=False),lease.command(),start,out)) for _ in range(2)]
    for w in workers:w.start()
    start.set();results=[out.get(timeout=15) for _ in workers]
    for w in workers:w.join(10);assert w.exitcode==0
    assert sum(x[0]=='ok' for x in results)==1,results
    assert not any(x[0]=='error' for x in results),results
    assert pg.repo.get(pg.p,job)['attempt_count']==2

def test_ex19_supervised_task_heartbeats_then_publishes(pg):
    from helpers import delayed_fixture_task
    from evidencetwin_backend.execution.worker import Worker
    settings=replace(pg.repo.settings,heartbeat_seconds=.05,heartbeat_timeout=.1,lease_seconds=2,stop_grace=.1)
    pg.db.settings=settings;pg.repo.settings=settings
    supervisor=Supervisor(settings);pg.repo.adapters=replace(pg.adapters,stop=supervisor)
    job=pg.repo.submit(pg.p,pg.snapshot,'s')
    assert Worker(pg.repo,pg.p,delayed_fixture_task,supervisor).once()
    assert pg.repo.get(pg.p,job)['state']=='succeeded'
    with pg.admin.connect() as c:assert c.execute(select(t.attempts.c.version)).scalar_one()>3

def test_ex18_worker_reconciles_same_heartbeat_operation_after_lost_ack(pg,monkeypatch):
    from helpers import delayed_fixture_task
    from evidencetwin_backend.execution.worker import Worker
    from evidencetwin_backend.execution.contracts import CommitUnknown
    settings=replace(pg.repo.settings,heartbeat_seconds=.03,heartbeat_timeout=.1,lease_seconds=2,stop_grace=.1)
    pg.db.settings=settings;pg.repo.settings=settings;s=Supervisor(settings)
    pg.repo.adapters=replace(pg.adapters,stop=s);job=pg.repo.submit(pg.p,pg.snapshot,'s')
    original=pg.repo.heartbeat;keys=[]
    def lost(p,lease,key):
        keys.append(key);renewed=original(p,lease,key)
        if len(keys)==1:raise CommitUnknown('commit_outcome_unknown')
        return renewed
    monkeypatch.setattr(pg.repo,'heartbeat',lost)
    assert Worker(pg.repo,pg.p,delayed_fixture_task,s).once()
    assert len(keys)>=2 and keys[0]==keys[1]
    assert pg.repo.get(pg.p,job)['state']=='succeeded'

def test_ex19_worker_honors_two_missed_heartbeats(pg,monkeypatch):
    from helpers import slow_task
    from evidencetwin_backend.execution.worker import Worker
    from evidencetwin_backend.execution.contracts import Contention
    settings=replace(pg.repo.settings,heartbeat_seconds=.03,heartbeat_timeout=.1,lease_seconds=2,stop_grace=.03)
    pg.db.settings=settings;pg.repo.settings=settings;s=Supervisor(settings)
    pg.repo.adapters=replace(pg.adapters,stop=s);job=pg.repo.submit(pg.p,pg.snapshot,'s');keys=[]
    def missed(p,lease,key):keys.append(key);raise Contention('database_contention')
    monkeypatch.setattr(pg.repo,'heartbeat',missed)
    assert Worker(pg.repo,pg.p,slow_task,s).once() is False
    assert len(keys)==2 and len(set(keys))==1
    assert pg.repo.get(pg.p,job)['state']=='running'
