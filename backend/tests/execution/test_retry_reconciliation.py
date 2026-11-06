from uuid import uuid4
import pytest
from sqlalchemy import select,func
from helpers import PAYLOAD
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.recovery import Recovery
from evidencetwin_backend.execution.contracts import Rejected

def test_ex25_three_total_attempts_persistent_steps_and_fences(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');r=Recovery(pg.repo,lambda a,b:0);fences=[]
    for i in range(3):
        lease=pg.repo.claim(pg.p,uuid4());fences.append(lease.fence)
        target=r.retire(pg.p,job,str(i),expected_version=lease.job_version,lease=lease,retryable=True,
            proof=pg.adapters.stop.proof(lease),reason='transient_preacceptance')
        assert target==('retry_wait' if i<2 else 'failed')
    assert fences==[1,2,3]
    assert pg.repo.get(pg.p,job)['attempt_count']==3
    assert pg.repo.claim(pg.p,uuid4()) is None

def test_ex29_30_reconciliation_does_not_clear_uncertain_calls(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());r=Recovery(pg.repo,lambda a,b:0)
    eid=r.external_intent(pg.p,lease,'i','call','test-provider-config')
    r.retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,retryable=True,proof=pg.adapters.stop.proof(lease),reason='transient_preacceptance')
    j=pg.repo.get(pg.p,job)
    assert r.reconcile(pg.p,job,'r',expected_version=j['version'],retry=True,authorization_ref='fixture-proof:replacement')=='retry_wait'
    new=pg.repo.claim(pg.p,uuid4())
    from evidencetwin_backend.execution.contracts import CapacityUnavailable
    with pytest.raises(CapacityUnavailable):r.external_intent(pg.p,new,'i2','replacement','test-provider-config')
    with pg.admin.connect() as c:assert c.execute(select(t.external_operations.c.settlement).where(t.external_operations.c.id==eid)).scalar_one()=='unresolved'

def test_ex25_retry_delay_stored_and_not_redrawn(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());calls=[]
    def draw(a,b):calls.append((a,b));return b
    r=Recovery(pg.repo,draw);proof=pg.adapters.stop.proof(lease)
    r.retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,retryable=True,proof=proof,reason='transient_preacceptance')
    with pg.admin.connect() as c:deadline=c.execute(select(t.queue_entries.c.ready_at).where(t.queue_entries.c.job_id==job)).scalar_one()
    r.retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,retryable=True,proof=proof,reason='transient_preacceptance')
    assert calls==[(0,2)]
    with pg.admin.connect() as c:assert c.execute(select(t.queue_entries.c.ready_at).where(t.queue_entries.c.job_id==job)).scalar_one()==deadline

def test_ex25_retry_after_not_shortened_to_jitter_cap(pg):
    from datetime import timedelta
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pg.admin.connect() as c:deadline=c.execute(select(func.clock_timestamp())).scalar_one()+timedelta(seconds=60)
    Recovery(pg.repo,lambda a,b:0).retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,retryable=True,
        proof=pg.adapters.stop.proof(lease),retry_not_before=deadline.isoformat(),reason='transient_preacceptance')
    with pg.admin.connect() as c:assert c.execute(select(t.queue_entries.c.ready_at).where(t.queue_entries.c.job_id==job)).scalar_one()==deadline
    assert pg.repo.claim(pg.p,uuid4()) is None

def test_ex25_permanent_failure_not_retried_even_if_requested(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    assert Recovery(pg.repo).retire(pg.p,job,'f',expected_version=lease.job_version,lease=lease,
        retryable=True,reason='input_invalid',proof=pg.adapters.stop.proof(lease))=='failed'
    assert pg.repo.get(pg.p,job)['attempt_count']==1
