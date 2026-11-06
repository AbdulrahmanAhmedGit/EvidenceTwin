from uuid import uuid4
from dataclasses import replace
import pytest
from sqlalchemy import select,insert,update,func
from helpers import PAYLOAD,principal
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.contracts import Rejected,IntegrationUnavailable,Adapters,canonical,digest
from evidencetwin_backend.execution.repository import Repository

def test_ex38_no_authorizer_fails_closed(pg):
    repo=Repository(pg.db)
    with pytest.raises(IntegrationUnavailable):repo.submit(pg.p,pg.snapshot,'s')

def test_ex39_owner_isolation_and_replay(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    with pytest.raises(Rejected):pg.repo.get(principal('bob'),job)
    with pytest.raises(Rejected):pg.repo.publish(principal('bob'),lease,'p',PAYLOAD)

def test_ex35_suspension_blocks_valid_worker_output(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    with pg.admin.begin() as c:
        key=c.execute(select(t.snapshots.c.authority_guard).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
        c.execute(update(t.guards).where(t.guards.c.key==key).values(eligible=False,version=2))
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    assert pg.repo.cancel(pg.p,job,'cancel',expected_version=lease.job_version)=='cancellation_requested'

def test_ex36_artifact_staging_and_deletion_guard(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());aid=uuid4();h=digest(b'fixture-artifact');key='artifact:'+str(aid)
    with pg.admin.begin() as c:
        c.execute(insert(t.guards).values(key=key,kind='artifact',owner_ref='alice',version=1,eligible=True,binding_sha256=h))
        c.execute(insert(t.artifacts).values(id=aid,owner_ref='alice',guard_key=key,object_ref='fixture:chart',object_version='1',
            sha256=h,byte_count=16,media_type='image/png',created_at=func.clock_timestamp()))
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.publication_artifacts)).scalar_one()==0
    pg.repo.publish(pg.p,lease,'step',PAYLOAD,step='fixture-chart',artifact_ids=[aid])
    with pg.admin.begin() as c:c.execute(update(t.guards).where(t.guards.c.key==key).values(eligible=False,version=2))
    with pytest.raises(Rejected):pg.repo.publish(pg.p,lease,'p',PAYLOAD,artifact_ids=[aid])

def test_ex41_canonical_rejects_float_and_overflow():
    for x in [1.5,float('nan'),{'data':'x'*262145}]:
        with pytest.raises(Rejected):canonical(x)

def test_ex39_historical_replay_denied_after_account_revocation(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4())
    pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    with pg.admin.begin() as c:
        key=c.execute(select(t.snapshots.c.authority_guard).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
        c.execute(update(t.guards).where(t.guards.c.key==key).values(eligible=False,version=2))
    with pytest.raises(Rejected,match='access_denied'):pg.repo.publish(pg.p,lease,'p',PAYLOAD)
    with pytest.raises(Rejected,match='access_denied'):pg.repo.get(pg.p,job)

def test_ex37_guard_type_cannot_exempt_mandatory_guard(pg):
    with pg.admin.begin() as c:
        key=c.execute(select(t.snapshots.c.authority_guard).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
        c.execute(update(t.guards).where(t.guards.c.key==key).values(kind='artifact'))
    with pytest.raises(Rejected,match='guard_kind'):pg.repo.submit(pg.p,pg.snapshot,'s')

def test_ex39_cross_owner_non_enumerating_not_found(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s')
    with pytest.raises(Rejected) as wrong:pg.repo.get(principal('bob'),job)
    with pytest.raises(Rejected) as missing:pg.repo.get(principal('bob'),uuid4())
    assert wrong.value.code==missing.value.code=='not_found'

def test_ex40_missing_physical_artifact_never_published(pg):
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());aid=uuid4();h=digest(b'missing');key='artifact:'+str(aid)
    with pg.admin.begin() as c:
        c.execute(insert(t.guards).values(key=key,kind='artifact',owner_ref='alice',version=1,eligible=True,binding_sha256=h))
        c.execute(insert(t.artifacts).values(id=aid,owner_ref='alice',guard_key=key,object_ref='missing:object',object_version='1',
            sha256=h,byte_count=7,media_type='image/png',created_at=func.clock_timestamp()))
    with pytest.raises(Rejected,match='artifact_not_ready'):pg.repo.publish(pg.p,lease,'p',PAYLOAD,artifact_ids=[aid])
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.publication_artifacts)).scalar_one()==0

def test_ex35_revocation_during_validation_cannot_publish_stale_authority(pg):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    job=pg.repo.submit(pg.p,pg.snapshot,'s');lease=pg.repo.claim(pg.p,uuid4());ready=threading.Event();release=threading.Event()
    original=pg.adapters.validator
    class PausedValidator:
        def validate(self,*args):
            result=original.validate(*args);ready.set();assert release.wait(5);return result
    pg.repo.adapters=replace(pg.adapters,validator=PausedValidator())
    with ThreadPoolExecutor(max_workers=1) as pool:
        future=pool.submit(pg.repo.publish,pg.p,lease,'p',PAYLOAD)
        try:
            assert ready.wait(5)
            with pg.admin.begin() as c:
                key=c.execute(select(t.snapshots.c.authority_guard).where(t.snapshots.c.id==pg.snapshot)).scalar_one()
                c.execute(update(t.guards).where(t.guards.c.key==key).values(eligible=False,version=2))
        finally:release.set()
        with pytest.raises(Rejected):future.result(timeout=5)
    with pg.admin.connect() as c:assert c.execute(select(func.count()).select_from(t.publications)).scalar_one()==0

def test_ex34_manifest_scope_cannot_disagree_with_snapshot_row(pg):
    with pg.admin.begin() as c:c.execute(update(t.snapshots).where(t.snapshots.c.id==pg.snapshot).values(analysis_revision='different'))
    with pytest.raises(Rejected,match='snapshot_scope_mismatch'):pg.repo.submit(pg.p,pg.snapshot,'s')
