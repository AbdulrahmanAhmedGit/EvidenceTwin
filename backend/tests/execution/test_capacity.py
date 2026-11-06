from uuid import uuid4
import pytest
from sqlalchemy import select,func,update
from helpers import PAYLOAD
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.recovery import Recovery
from evidencetwin_backend.execution.contracts import CapacityUnavailable

def test_ex29_30_31_uncertain_calls_hold_all_request_permits(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());r=Recovery(pg.repo)
    external=r.external_intent(pg.p,lease,'intent','call1','test-provider-config')
    with pytest.raises(CapacityUnavailable):r.external_intent(pg.p,lease,'intent2','call2','test-provider-config')
    proof=pg.adapters.stop.proof(lease)
    assert r.retire(pg.p,lease.job_id,'failure',expected_version=lease.job_version,lease=lease,retryable=True,proof=proof,reason='transient_preacceptance')=='reconciliation_required'
    with pg.admin.connect() as c:
        scopes={x['key']:x['in_use'] for x in c.execute(select(t.capacity_scopes)).mappings()}
        assert scopes['analyses']==0 and scopes['global_llm']==1
    assert r.settle(pg.p,lease.job_id,external,'settle',outcome='completed',evidence_ref='fixture-proof:late')=='completed'
    assert r.settle(pg.p,lease.job_id,external,'settle',outcome='completed',evidence_ref='fixture-proof:late')=='completed'
    with pg.admin.connect() as c:assert c.execute(select(t.capacity_scopes.c.in_use).where(t.capacity_scopes.c.key=='global_llm')).scalar_one()==0
    assert pg.repo.get(pg.p,lease.job_id)['state']=='reconciliation_required'

def test_ex33_lowering_capacity_below_live_usage_rejected(pg):
    from sqlalchemy.exc import IntegrityError
    pg.repo.submit(pg.p,pg.snapshot,'s');pg.repo.claim(pg.p,uuid4())
    with pytest.raises(IntegrityError):
        with pg.admin.begin() as c:c.execute(update(t.capacity_scopes).where(t.capacity_scopes.c.key=='analyses').values(capacity=0))

def test_ex11_final_without_stop_proof_conservatively_holds_analysis_capacity(pg):
    pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    with pg.admin.connect() as c:assert c.execute(select(t.capacity_scopes.c.in_use).where(t.capacity_scopes.c.key=='analyses')).scalar_one()==1

def test_ex32_cancelled_job_settles_without_reopening(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());r=Recovery(pg.repo)
    eid=r.external_intent(pg.p,lease,'i','call','test-provider-config')
    pg.repo.cancel(pg.p,job,'cancel',expected_version=lease.job_version)
    j=pg.repo.get(pg.p,job)
    r.finalize_cancel(pg.p,job,'finish',expected_version=j['version'],proof=pg.adapters.stop.proof(lease))
    assert r.settle(pg.p,job,eid,'late',outcome='completed',evidence_ref='fixture-proof:late')=='completed'
    assert pg.repo.get(pg.p,job)['state']=='cancelled'

def test_ex11_analysis_limit_shared_across_three_processes(pg):
    import multiprocessing as mp
    from helpers import claim_process
    for i in range(3):pg.repo.submit(pg.p,pg.snapshot,str(i))
    ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    workers=[ctx.Process(target=claim_process,args=(pg.url.render_as_string(hide_password=False),'alice',start,out)) for _ in range(3)]
    for w in workers:w.start()
    start.set();results=[out.get(timeout=15) for _ in workers]
    for w in workers:w.join(10);assert w.exitcode==0
    assert sum(x[0]=='ok' and x[1] is not None for x in results)==2,results
    assert sum(x==('rejected','capacity_full') for x in results)==1,results
    with pg.admin.connect() as c:assert c.execute(select(t.capacity_scopes.c.in_use).where(t.capacity_scopes.c.key=='analyses')).scalar_one()==2

def test_ex29_global_provider_requests_bounded_across_processes(pg):
    import multiprocessing as mp
    from helpers import external_intent_process
    # Test-only larger analysis capacity isolates the independent global request cap.
    with pg.admin.begin() as c:c.execute(update(t.capacity_scopes).where(t.capacity_scopes.c.key=='analyses').values(capacity=3))
    for i in range(3):pg.repo.submit(pg.p,pg.snapshot,str(i))
    leases=[pg.repo.claim(pg.p,uuid4()) for _ in range(3)]
    ctx=mp.get_context('spawn');start=ctx.Event();out=ctx.Queue()
    workers=[ctx.Process(target=external_intent_process,args=(pg.url.render_as_string(hide_password=False),lease.command(),start,out)) for lease in leases]
    for w in workers:w.start()
    start.set();results=[out.get(timeout=15) for _ in workers]
    for w in workers:w.join(10);assert w.exitcode==0
    assert sum(x[0]=='ok' for x in results)==2,results
    assert sum(x==('rejected','capacity_full') for x in results)==1,results
    with pg.admin.connect() as c:
        assert c.execute(select(t.capacity_scopes.c.in_use).where(t.capacity_scopes.c.key=='global_llm')).scalar_one()==2
        assert c.execute(select(func.count()).select_from(t.external_operations)).scalar_one()==2
