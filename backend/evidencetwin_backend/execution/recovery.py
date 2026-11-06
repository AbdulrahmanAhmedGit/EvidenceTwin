"""Guarded execution recovery; never sends or automatically repeats provider calls."""
from datetime import timedelta, datetime
import random
from uuid import uuid4, UUID
from sqlalchemy import select, insert, update, func
from . import tables as t, capacity
from .contracts import Rejected, IntegrationUnavailable, canonical
from .transitions import allowed

class Recovery:

    def __init__(self, repository, random_uniform=None):
        self.r = repository
        self.uniform = random_uniform or random.uniform

    def _scopes(self, c, j):
        keys = [x[0] for x in c.execute(select(t.reservations.c.scope_key).where(t.reservations.c.job_id == j['id'], t.reservations.c.released_at.is_(None)))]
        capacity.lock_scopes(c, keys)

    def _stop(self, c, j, a, proof):
        if proof is None:
            return False
        verifier = self.r.adapters.stop
        if verifier is None or proof.instance != a['owner_instance'] or (not verifier.stopped(proof, a)):
            raise Rejected('stop_proof_invalid')
        capacity.release(c, j['id'], a['id'], proof.evidence_ref, analyses_only=True)
        return True

    def _schedule(self, c, j, now, not_before=None):
        if j['attempt_count'] >= j['max_attempts']:
            raise Rejected('attempt_limit')
        ordinal = j['attempt_count'] + 1
        aid = uuid4()
        upper = min(self.r.settings.retry_cap, self.r.settings.retry_base * 2 ** (j['attempt_count'] - 1))
        delay = self.uniform(0, upper)
        if not 0 <= delay <= upper:
            raise Rejected('invalid_retry_jitter')
        c.execute(insert(t.attempts).values(id=aid, job_id=j['id'], ordinal=ordinal, state='pending', version=1, created_at=now))
        _checked(c, update(t.jobs).where(t.jobs.c.id == j['id']).values(current_attempt_id=aid, attempt_count=ordinal))
        _checked(c, update(t.queue_entries).where(t.queue_entries.c.job_id == j['id']).values(enabled=True, pending_attempt_id=aid, ready_at=max(now+timedelta(seconds=delay),not_before or now), version=t.queue_entries.c.version + 1))
        return aid

    def retire(self, p, job_id, key, *, expected_version, lease=None, retryable=False, proof=None, reason='permanent_execution_error', expected_attempt_id=None, expected_fence=None, retry_not_before=None):
        """Worker failure or controller lease recovery. Retryability is an explicit service decision.

        An unresolved operation always overrides retryable=True. The repository never
        infers safe paid replay from a generic exception, timeout or HTTP status.
        """
        if lease is None and (expected_attempt_id is None or expected_fence is None):raise Rejected('recovery_context_required')
        transient={'transient_preacceptance','transient_settled_provider','provider_throttled_settled','lease_expired'}
        causes=transient|{'permanent_execution_error','input_invalid','configuration_unavailable','external_outcome_uncertain'}
        if reason not in causes:raise Rejected('unknown_failure_cause')
        if lease is None and reason=='permanent_execution_error':reason='lease_expired'
        retryable=bool(retryable and reason in transient)
        not_before=None
        if retry_not_before is not None:
            try:not_before=datetime.fromisoformat(retry_not_before)
            except (ValueError,TypeError):raise Rejected('invalid_retry_deadline') from None
            if not_before.tzinfo is None:raise Rejected('invalid_retry_deadline')
        body = {'version': expected_version, 'lease': lease.command() if lease else None, 'retryable': retryable, 'reason': reason, 'proof': proof.evidence_ref if proof else None,
            'expected_attempt_id':str(expected_attempt_id) if expected_attempt_id else None,'expected_fence':expected_fence,'retry_not_before':retry_not_before}
        r = self.r

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'worker_failure' if lease else 'recover', eligible=False)
            old, data = r._op(c, p, job_id, 'retire', key, body)
            if old:
                return old['state']
            if j['version'] != expected_version:
                raise Rejected('stale_revision')
            if lease:
                r._guards(c, s)
            self._scopes(c, j)
            if lease:
                a, now = r._owned(c, j, lease)
            else:
                a = dict(c.execute(select(t.attempts).where(t.attempts.c.id == j['current_attempt_id']).with_for_update()).mappings().one())
                now = c.execute(select(func.clock_timestamp())).scalar_one()
                if a['id']!=expected_attempt_id or a['fence']!=expected_fence or j['fence_counter']!=expected_fence:raise Rejected('stale_execution')
                if j['state'] != 'running' or a['state'] != 'running' or a['lease_until'] > now:
                    raise Rejected('lease_not_expired')
            uncertain = bool(c.execute(select(t.external_operations.c.id).where(t.external_operations.c.job_id == job_id, t.external_operations.c.settlement == 'unresolved')).first())
            target = 'reconciliation_required' if uncertain else 'retry_wait' if retryable and j['attempt_count'] < j['max_attempts'] else 'failed'
            worker = lease is not None
            astate = 'failed' if worker else 'abandoned'
            edge = ({'retry_wait': 'J05', 'failed': 'J06', 'reconciliation_required': 'J09'} if worker else {'retry_wait': 'J07', 'failed': 'J08', 'reconciliation_required': 'J10'})[target]
            allowed(edge, j['state'], target, 'worker' if worker else 'recovery', a['state'], astate)
            self._stop(c, j, a, proof)
            _checked(c, update(t.attempts).where(t.attempts.c.id == a['id'], t.attempts.c.version == a['version']).values(state=astate, lease_until=None, ended_at=now, failure_code=reason, version=a['version'] + 1))
            _checked(c, update(t.jobs).where(t.jobs.c.id == job_id, t.jobs.c.version == expected_version).values(state=target, failure_code=reason, version=j['version'] + 1, updated_at=now))
            if target == 'retry_wait':
                self._schedule(c, j, now,not_before)
            r._finish(c, p, job_id, 'retire', key, data, {'state': target}, job_id)
            r._pair(c, job_id)
            return target
        return r._run(p, job_id, 'retire', key, body, run)

    def finalize_cancel(self, p, job_id, key, *, expected_version, proof=None):
        r = self.r
        body = {'version': expected_version, 'proof': proof.evidence_ref if proof else None}

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'finalize_cancel', eligible=False)
            old, data = r._op(c, p, job_id, 'finalize_cancel', key, body)
            if old:
                return old['state']
            if j['version'] != expected_version:
                raise Rejected('stale_revision')
            self._scopes(c, j)
            a = dict(c.execute(select(t.attempts).where(t.attempts.c.id == j['current_attempt_id']).with_for_update()).mappings().one())
            allowed('J17', j['state'], 'cancelled', 'cancellation', a['state'], 'cancelled')
            self._stop(c, j, a, proof)
            now = c.execute(select(func.clock_timestamp())).scalar_one()
            _checked(c, update(t.attempts).where(t.attempts.c.id == a['id']).values(state='cancelled', lease_until=None, ended_at=now, version=a['version'] + 1))
            _checked(c, update(t.jobs).where(t.jobs.c.id == job_id).values(state='cancelled', version=j['version'] + 1, updated_at=now))
            r._finish(c, p, job_id, 'finalize_cancel', key, data, {'state': 'cancelled'}, job_id)
            r._pair(c, job_id)
            return 'cancelled'
        return r._run(p, job_id, 'finalize_cancel', key, body, run)

    def release_stopped(self, p, job_id, proof):
        r = self.r

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'stop_evidence', eligible=False)
            self._scopes(c, j)
            a = c.execute(select(t.attempts).where(t.attempts.c.job_id == job_id, t.attempts.c.owner_instance == proof.instance)).mappings().first()
            if not a or a['state'] not in {'failed', 'abandoned', 'cancelled'}:
                raise Rejected('stop_target_invalid')
            self._stop(c, j, a, proof)
            r._audit(c, p, 'execution_stopped', job_id, attempt=a['id'])
        r.db.run(run)

    def reconcile(self, p, job_id, key, *, expected_version, retry, authorization_ref):
        r = self.r
        body = {'version': expected_version, 'retry': retry, 'authorization_ref': authorization_ref}
        if not isinstance(authorization_ref, str) or not 0 < len(authorization_ref) <= 512:
            raise Rejected('authorization_reference_required')

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'reconcile', eligible=retry)
            old, data = r._op(c, p, job_id, 'reconcile', key, body)
            if old:
                return old['state']
            if j['version'] != expected_version:
                raise Rejected('stale_revision')
            target = 'retry_wait' if retry and j['attempt_count'] < j['max_attempts'] else 'failed'
            allowed('J11' if target == 'retry_wait' else 'J12', j['state'], target, 'reconciliation')
            now = c.execute(select(func.clock_timestamp())).scalar_one()
            _checked(c, update(t.jobs).where(t.jobs.c.id == job_id).values(state=target, version=j['version'] + 1, updated_at=now))
            if target == 'retry_wait':
                self._schedule(c, j, now)
            r._finish(c, p, job_id, 'reconcile', key, data, {'state': target}, job_id)
            r._audit(c, p, 'replacement_authorization', job_id, authorization_ref=authorization_ref)
            r._pair(c, job_id)
            return target
        return r._run(p, job_id, 'reconcile', key, body, run)

    def scheduling_stop(self, p, job_id, key, *, expected_version):
        r = self.r
        body = {'version': expected_version}

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'scheduling_stop', eligible=False)
            old, data = r._op(c, p, job_id, 'scheduling_stop', key, body)
            if old:
                return old['state']
            if j['version'] != expected_version:
                raise Rejected('stale_revision')
            a = c.execute(select(t.attempts).where(t.attempts.c.id == j['current_attempt_id'])).mappings().one()
            allowed('J18' if j['state'] == 'queued' else 'J19', j['state'], 'failed', 'controller', a['state'], 'cancelled')
            now = c.execute(select(func.clock_timestamp())).scalar_one()
            _checked(c, update(t.attempts).where(t.attempts.c.id == a['id']).values(state='cancelled', ended_at=now, version=a['version'] + 1))
            _checked(c, update(t.jobs).where(t.jobs.c.id == job_id).values(state='failed', failure_code='scheduling_stopped', version=j['version'] + 1, updated_at=now))
            _checked(c, update(t.queue_entries).where(t.queue_entries.c.job_id == job_id).values(enabled=False, pending_attempt_id=None, version=t.queue_entries.c.version + 1))
            r._finish(c, p, job_id, 'scheduling_stop', key, data, {'state': 'failed'}, job_id)
            r._pair(c, job_id)
            return 'failed'
        return r._run(p, job_id, 'scheduling_stop', key, body, run)

    def external_intent(self, p, lease, key, logical_key, provider_ref):
        """Persist intent/reservations only. Never sends a request."""
        r = self.r
        body = {'lease': lease.command(), 'logical_key': logical_key, 'provider_ref': provider_ref}
        if r.adapters.spend is None:
            raise IntegrationUnavailable('spend_adapter_unavailable')
        spend_ref = r.adapters.spend.approve(p, logical_key, provider_ref)
        if not spend_ref:
            raise Rejected('spend_denied')

        def run(c):
            j, s, m, q = r._context(c, p, lease.job_id, 'external_intent', eligible=False)
            old, data = r._op(c, p, j['id'], 'external_intent', key, body)
            if old:
                return UUID(old['external_id'])
            r._guards(c, s)
            keys = ['analysis_llm:' + str(j['id']), 'global_llm', 'provider:' + provider_ref]
            capacity.lock_scopes(c, keys)
            a, now = r._owned(c, j, lease)
            if provider_ref != m.get('provider_configuration_ref'):
                raise Rejected('pinned_provider_mismatch')
            eid = uuid4()
            c.execute(insert(t.external_operations).values(id=eid, job_id=j['id'], attempt_id=a['id'], fence=a['fence'], logical_key=logical_key, step_key=logical_key, provider_configuration_ref=provider_ref, settlement='unresolved', dispatch_intent_at=now, version=1))
            capacity.reserve(c, keys, j['id'], a['id'], 'external:' + str(eid), eid)
            r._finish(c, p, j['id'], 'external_intent', key, data, {'external_id': str(eid)}, j['id'])
            r._audit(c, p, 'spend_authorized', j['id'], spend_reference=spend_ref)
            return eid
        return r._run(p, lease.job_id, 'external_intent', key, body, run)

    def settle(self, p, job_id, eid, key, *, outcome, evidence_ref):
        r = self.r
        body = {'external': str(eid), 'outcome': outcome, 'evidence_ref': evidence_ref}
        if outcome not in {'not_sent', 'completed', 'failed'}:
            raise Rejected('settlement_outcome')
        verifier = r.adapters.settlement
        if verifier is None:
            raise IntegrationUnavailable('settlement_adapter_unavailable')

        def prepare(c):
            j, s, m, q = r._context(c, p, job_id, 'settle', eligible=False)
            e = c.execute(select(t.external_operations).where(t.external_operations.c.id == eid, t.external_operations.c.job_id == job_id)).mappings().first()
            if not e:
                raise Rejected('not_found')
            return dict(e)
        e = r.db.run(prepare)
        if not verifier.verify(e, outcome, evidence_ref, p):
            raise Rejected('settlement_evidence_invalid')

        def run(c):
            j, s, m, q = r._context(c, p, job_id, 'settle', eligible=False)
            old, data = r._op(c, p, job_id, 'settle', key, body)
            if old:
                return old['outcome']
            self._scopes(c, j)
            current = c.execute(select(t.external_operations).where(t.external_operations.c.id == eid).with_for_update()).mappings().one()
            if current['version'] != e['version'] or current['settlement'] != 'unresolved':
                raise Rejected('settlement_conflict')
            _checked(c, update(t.external_operations).where(t.external_operations.c.id == eid, t.external_operations.c.version == e['version']).values(settlement=outcome, observed_at=func.clock_timestamp(), version=e['version'] + 1))
            capacity.release(c, job_id, e['attempt_id'], evidence_ref, external=eid)
            r._finish(c, p, job_id, 'settle', key, data, {'outcome': outcome}, job_id)
            r._audit(c, p, 'external_settled', job_id, attempt=e['attempt_id'], outcome=outcome, evidence_ref=evidence_ref)
            return outcome
        return r._run(p, job_id, 'settle', key, body, run)

def _checked(c,statement):
    result=c.execute(statement)
    if result.rowcount!=1:raise Rejected('conditional_write_rejected')
    return result
