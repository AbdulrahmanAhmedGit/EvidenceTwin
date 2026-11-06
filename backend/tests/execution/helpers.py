"""Explicit test-only authorizers, validators and controlled processes. Never production."""
from dataclasses import replace
from uuid import uuid4, UUID
import json
import time
from sqlalchemy import select, insert, update, func
from evidencetwin_backend.execution import tables as t
from evidencetwin_backend.execution.contracts import Principal,Adapters,Rejected,StopProof,canonical,digest
from evidencetwin_backend.execution.database import Database
from evidencetwin_backend.execution.repository import Repository
from evidencetwin_backend.execution.settings import Settings

PAYLOAD=b'{"fixture":true,"message":"Synthetic infrastructure task; no scientific assessment."}'
class TestAuthorizer:
    def authorize(self,p,action,s):
        if action=='claim' and p.actor_ref=='fixture-dispatcher' and 'dispatcher' in p.roles:return True
        if p.owner_ref!=s['owner_ref']:return False
        if action in {'recover','finalize_cancel','stop_evidence','reconcile','scheduling_stop','settle'}:
            return 'controller' in p.roles
        return 'researcher' in p.roles
class TestValidator:
    def validate(self,payload,snapshot,kind):
        if json.loads(payload).get('fixture') is not True:raise Rejected('fixture_schema_invalid')
        return digest(payload+bytes(snapshot['manifest_sha256'])+kind.encode())
class TestArtifacts:
    def ready(self,artifact,snapshot):return artifact['object_ref'].startswith('fixture:')
class TestStops:
    def __init__(self):self.proofs={}
    def proof(self,lease):
        p=StopProof(lease.owner_instance,'fixture-stop:'+uuid4().hex);self.proofs[p.evidence_ref]=p.instance;return p
    def stopped(self,proof,attempt):return self.proofs.get(proof.evidence_ref)==attempt['owner_instance']
class TestSettlement:
    def verify(self,op,outcome,evidence,p):return evidence.startswith('fixture-proof:') and 'controller' in p.roles
class TestSpend:
    def approve(self,p,logical,provider):return 'fixture-spend:'+logical

def principal(owner='alice'):return Principal(owner,'fixture-researcher',frozenset({'researcher','controller'}))
def adapters(stops=None):return Adapters(TestAuthorizer(),TestValidator(),TestArtifacts(),stops or TestStops(),TestSettlement(),TestSpend())
def fixture_task():return PAYLOAD
def slow_task():time.sleep(60);return PAYLOAD

def seed_snapshot(admin,p=None):
    p=p or principal();sid=uuid4();case='fixture-case:'+uuid4().hex;analysis='fixture-analysis:'+uuid4().hex;guards={};cols={}
    for col,kind in [('authority_guard','authority'),('case_guard','case'),('evidence_guard','snapshot'),('policy_guard','policy'),('configuration_guard','configuration')]:
        key=kind+':'+str(sid);h=digest(key.encode());guards[key]={'version':1,'sha256':h.hex()}
        admin.execute(insert(t.guards).values(key=key,kind=kind,owner_ref=p.owner_ref,version=1,eligible=True,binding_sha256=h));cols[col]=key
    manifest=canonical({'owner_ref':p.owner_ref,'case_ref':case,'analysis_ref':analysis,'analysis_revision':'fixture-v1','schema':'execution-snapshot-v1','guards':guards,'evidence_snapshot_ref':str(uuid4()),'manifest_revision':'fixture-v1',
        'classification_revision':'fixture-confirmed','policy_ref':'fixture-policy','execution_config':'fixture-config','output_schema':'execution-test-output-v1','provider_configuration_ref':'test-provider-config'})
    admin.execute(insert(t.snapshots).values(id=sid,owner_ref=p.owner_ref,case_ref=case,analysis_ref=analysis,
        analysis_revision='fixture-v1',schema_ref='execution-snapshot-v1',manifest=manifest,manifest_sha256=digest(manifest),created_at=func.clock_timestamp(),**cols))
    return sid

def claim_process(url,owner,start,out):
    db=Database(url);repo=Repository(db,adapters())
    try:
        start.wait(10);lease=repo.claim(principal(owner),uuid4());out.put(('ok',lease.command() if lease else None))
    except Rejected as e:out.put(('rejected',e.code))
    except Exception as e:out.put(('error',type(e).__name__))
    finally:db.close()

def race_process(url,pdata,lease_data,kind,start,out):
    from evidencetwin_backend.execution.contracts import Lease
    db=Database(url);repo=Repository(db,adapters());p=principal(pdata);lease=Lease.restore(lease_data)
    try:
        start.wait(10)
        if kind=='publish':repo.publish(p,lease,'race-publish',PAYLOAD)
        else:repo.cancel(p,lease.job_id,'race-cancel',expected_version=lease.job_version)
        out.put(('ok',kind))
    except Rejected as e:out.put(('rejected',e.code))
    except Exception as e:out.put(('error',type(e).__name__))
    finally:db.close()

def lock_queue_process(url,job,ready,release):
    db=Database(url)
    try:
        with db.engine.begin() as c:
            c.execute(select(t.queue_entries).where(t.queue_entries.c.job_id==UUID(job)).with_for_update());ready.set();release.wait(5)
    finally:db.close()

def recovery_process(url,lease_data,start,out):
    from evidencetwin_backend.execution.contracts import Lease
    from evidencetwin_backend.execution.recovery import Recovery
    db=Database(url);a=adapters();repo=Repository(db,a);lease=Lease.restore(lease_data)
    try:
        start.wait(10)
        result=Recovery(repo,lambda a,b:0).retire(principal(),lease.job_id,uuid4().hex,
            expected_version=lease.job_version,expected_attempt_id=lease.attempt_id,expected_fence=lease.fence,retryable=True,proof=a.stop.proof(lease))
        out.put(('ok',result))
    except Rejected as e:out.put(('rejected',e.code))
    except Exception as e:out.put(('error',type(e).__name__))
    finally:db.close()

def delayed_fixture_task():
    time.sleep(.3)
    return PAYLOAD

def external_intent_process(url,lease_data,start,out):
    from evidencetwin_backend.execution.contracts import Lease
    from evidencetwin_backend.execution.recovery import Recovery
    db=Database(url);repo=Repository(db,adapters());lease=Lease.restore(lease_data)
    try:
        start.wait(10)
        result=Recovery(repo).external_intent(principal(),lease,'intent','call','test-provider-config')
        out.put(('ok',str(result)))
    except Rejected as e:out.put(('rejected',e.code))
    except Exception as e:out.put(('error',type(e).__name__))
    finally:db.close()

def pending_race_process(url,job,kind,start,out):
    db=Database(url);repo=Repository(db,adapters())
    try:
        start.wait(10)
        if kind=='claim':out.put(('claim',repo.claim(principal(),uuid4()) is not None))
        else:out.put(('cancel',repo.cancel(principal(),UUID(job),'cancel',expected_version=1)))
    except Rejected as e:out.put(('rejected',e.code))
    except Exception as e:out.put(('error',type(e).__name__))
    finally:db.close()
