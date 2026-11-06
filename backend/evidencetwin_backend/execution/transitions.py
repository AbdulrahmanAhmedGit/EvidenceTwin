"""Complete, centralized Job/Attempt transition eligibility and paired validation."""
from .contracts import Rejected

# ID: (source, target, actor, attempt source, attempt target)
EDGES = {
 'J01':(None,'queued','admission',None,'pending'),
 'J02':('queued','running','dispatcher','pending','running'),
 'J03':('retry_wait','running','dispatcher','pending','running'),
 'J04':('running','succeeded','worker','running','succeeded'),
 'J05':('running','retry_wait','worker','running','failed'),
 'J06':('running','failed','worker','running','failed'),
 'J07':('running','retry_wait','recovery','running','abandoned'),
 'J08':('running','failed','recovery','running','abandoned'),
 'J09':('running','reconciliation_required','worker','running','failed'),
 'J10':('running','reconciliation_required','recovery','running','abandoned'),
 'J11':('reconciliation_required','retry_wait','reconciliation',None,None),
 'J12':('reconciliation_required','failed','reconciliation',None,None),
 'J13':('queued','cancelled','cancellation','pending','cancelled'),
 'J14':('retry_wait','cancelled','cancellation','pending','cancelled'),
 'J15':('reconciliation_required','cancelled','cancellation',None,None),
 'J16':('running','cancellation_requested','cancellation','running','cancellation_requested'),
 'J17':('cancellation_requested','cancelled','cancellation','cancellation_requested','cancelled'),
 'J18':('queued','failed','controller','pending','cancelled'),
 'J19':('retry_wait','failed','controller','pending','cancelled'),
}
TERMINAL={'succeeded','failed','cancelled'}
ATTEMPT_TERMINAL={'succeeded','failed','cancelled','abandoned'}

def allowed(event,source,target,actor,attempt_source=None,attempt_target=None):
    if EDGES.get(event)!=(source,target,actor,attempt_source,attempt_target):
        raise Rejected('invalid_transition')

def validate_pair(job,attempts,queue):
    active=[a for a in attempts if a['state'] not in ATTEMPT_TERMINAL]
    current=next((a for a in attempts if a['id']==job['current_attempt_id']),None)
    if current is None or any(a['job_id']!=job['id'] for a in attempts): raise Rejected('attempt_identity')
    if len(attempts)!=job['attempt_count'] or sorted(a['ordinal'] for a in attempts)!=list(range(1,len(attempts)+1)):
        raise Rejected('attempt_coverage')
    if job['attempt_count']>job['max_attempts']: raise Rejected('attempt_limit')
    wanted={'queued':'pending','retry_wait':'pending','running':'running','cancellation_requested':'cancellation_requested'}
    if job['state'] in wanted:
        if len(active)!=1 or active[0]['id']!=current['id'] or current['state']!=wanted[job['state']]:
            raise Rejected('paired_state')
    elif active: raise Rejected('terminal_active_attempt')
    if job['state']=='succeeded' and (current['state']!='succeeded' or not job['final_publication_id']):
        raise Rejected('missing_final_result')
    if job['state']=='reconciliation_required' and current['state'] not in {'failed','abandoned'}:
        raise Rejected('reconciliation_attempt')
    if job['state']=='failed' and current['state'] not in {'failed','abandoned','cancelled'}:
        raise Rejected('failed_attempt')
    if job['state']=='cancelled' and current['state'] not in {'failed','abandoned','cancelled'}:
        raise Rejected('cancelled_attempt')
    enabled=job['state'] in {'queued','retry_wait'}
    if queue['job_id']!=job['id'] or queue['owner_ref']!=job['owner_ref'] or queue['enabled']!=enabled:
        raise Rejected('queue_state')
    if queue['pending_attempt_id']!=(current['id'] if enabled else None): raise Rejected('queue_attempt')
