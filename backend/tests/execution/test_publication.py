import multiprocessing as mp
from uuid import uuid4
from dataclasses import replace
import pytest
from sqlalchemy import select,func,update
from helpers import PAYLOAD,race_process
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.contracts import Rejected,Conflict,IntegrationUnavailable

def test_ex06_20_27_final_lost_ack_replays_even_when_terminal(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    proof=pg.adapters.stop.proof(lease)
    pid=pg.repo.publish(pg.p,lease,'p',PAYLOAD,stop_proof=proof)
    assert pg.repo.publish(pg.p,lease,'p',PAYLOAD,stop_proof=proof)==pid
    with pytest.raises(Conflict):pg.repo.publish(pg.p,lease,'p',b'{"fixture":true,"different":true}',stop_proof=proof)
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.publications)).scalar_one()==1

def test_ex21_cancellation_publication_race_processes(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    processes=[ctx.Process(target=race_process,args=(pg.url.render_as_string(hide_password=False),'alice',lease.command(),kind,start,out)) for kind in ['publish','cancel']]
    for p in processes:p.start()
    start.set();results=[out.get(timeout=15) for _ in processes]
    for p in processes:p.join(10);assert p.exitcode==0
    assert not any(x[0]=='error' for x in results),results
    assert sum(x[0]=='ok' for x in results)==1,results
    j=pg.repo.get(pg.p,lease.job_id);assert j['state'] in {'succeeded','cancellation_requested'}
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.publications)).scalar_one()==(j['state']=='succeeded')

def test_ex34_policy_change_blocks_publication(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pg.admin.begin() as c:
        key=c.execute(select(t.snapshots.c.policy_guard).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
        c.execute(update(t.guards).where(t.guards.c.key==key).values(version=2))
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    assert pg.repo.get(pg.p,lease.job_id)['state']=='running'

def test_ex37_whole_payload_validation(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'p',b'{"verdict":"partially_supported"}')

def test_ex38_validator_unavailable(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    pg.repo.adapters=replace(pg.adapters,validator=None)
    with pytest.raises(IntegrationUnavailable):pg.repo.publish(pg.p,lease,'p',PAYLOAD)
