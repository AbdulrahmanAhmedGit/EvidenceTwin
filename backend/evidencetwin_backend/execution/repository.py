"""Explicit Core repositories. No scientific calculation or public HTTP integration."""
from datetime import timedelta
from uuid import uuid4, UUID
import json
from sqlalchemy import select, insert, update, func, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from . import tables as t, capacity
from .contracts import Adapters, Lease, Rejected, Conflict, IntegrationUnavailable, CapacityUnavailable, canonical, digest
from .transitions import allowed, validate_pair
MAX_COUNTER = 9223372036854775807

class Repository:

    def __init__(self, database, adapters=None):
        self.db = database
        self.settings = database.settings
        self.adapters = adapters or Adapters()

    def _audit(self, c, p, event, job=None, operation=None, attempt=None, **data):
        c.execute(insert(t.audit_events).values(id=uuid4(), job_id=job, operation_id=operation, attempt_id=attempt, actor_ref=p.actor_ref, event_type=event, safe_metadata=data, correlation_ref=uuid4(), occurred_at=func.clock_timestamp()))

    def _snapshot(self, c, snapshot_id):
        r = c.execute(select(t.snapshots).where(t.snapshots.c.id == snapshot_id)).mappings().first()
        if not r:
            raise Rejected('not_found')
        return dict(r)

    def _guards(self, c, snapshot, *, eligible=True):
        manifest = json.loads(bytes(snapshot['manifest']))
        keys = [snapshot[k] for k in ('authority_guard', 'case_guard', 'evidence_guard', 'policy_guard', 'configuration_guard')]
        required = {'owner_ref','case_ref','analysis_ref','analysis_revision','schema', 'guards', 'evidence_snapshot_ref', 'manifest_revision', 'classification_revision', 'policy_ref', 'execution_config', 'output_schema', 'provider_configuration_ref'}
        if not isinstance(manifest, dict) or not required.issubset(manifest) or manifest['schema'] != 'execution-snapshot-v1':
            raise Rejected('snapshot_schema')
        for field in ('owner_ref','case_ref','analysis_ref','analysis_revision'):
            if manifest[field]!=snapshot[field]:raise Rejected('snapshot_scope_mismatch')
        for field in required-{'guards'}:
            if not isinstance(manifest[field],str) or not 0<len(manifest[field])<=512:raise Rejected('snapshot_reference')
        if canonical(manifest) != bytes(snapshot['manifest']):
            raise Rejected('snapshot_canonical')
        refs = manifest.get('guards', {})
        if not isinstance(refs,dict) or set(refs)!=set(keys):raise Rejected('guard_contract')
        for value in refs.values():
            if (not isinstance(value,dict) or set(value)!={'version','sha256'}
                or type(value['version']) is not int or value['version']<=0
                or not isinstance(value['sha256'],str) or len(value['sha256'])!=64):raise Rejected('guard_contract')
        expected_kinds = dict(zip(keys, ('authority', 'case', 'snapshot', 'policy', 'configuration')))
        if len(set(keys)) != 5:
            raise Rejected('guard_identity')
        rank = {'authority': 0, 'case': 1, 'snapshot': 2, 'policy': 3, 'configuration': 4, 'artifact': 5}
        preview = list(c.execute(select(t.guards).where(t.guards.c.key.in_(keys))).mappings())
        if len(preview) != len(set(keys)):
            raise Rejected('guard_missing')
        for row in sorted(preview, key=lambda r: (rank[r['kind']], r['key'])):
            g = c.execute(select(t.guards).where(t.guards.c.key == row['key']).with_for_update()).mappings().one()
            if g['kind'] != row['kind'] or g['kind'] != expected_kinds[g['key']]:
                raise Rejected('guard_kind')
            owners = {snapshot['owner_ref']} if g['kind'] in {'authority', 'case'} else {None, snapshot['owner_ref']}
            if g['owner_ref'] not in owners:
                raise Rejected('guard_owner')
            if eligible:
                expected = refs.get(g['key'])
                if not expected or not g['eligible'] or g['version'] != expected['version'] or (bytes(g['binding_sha256']).hex() != expected['sha256']):
                    raise Rejected('guard_changed')
        if digest(bytes(snapshot['manifest'])) != bytes(snapshot['manifest_sha256']):
            raise Rejected('snapshot_integrity')
        return manifest

    def _context(self, c, p, job_id, action, *, eligible=True):
        q = c.execute(select(t.queue_entries).where(t.queue_entries.c.job_id == job_id).with_for_update()).mappings().first()
        if not q:
            raise Rejected('not_found')
        j = c.execute(select(t.jobs).where(t.jobs.c.id == job_id)).mappings().one()
        if action!='claim' and j['owner_ref']!=p.owner_ref:raise Rejected('not_found')
        snapshot = self._snapshot(c, j['snapshot_id'])
        self.adapters.authorize(p, action, snapshot)
        manifest = self._guards(c, snapshot, eligible=eligible)
        cleanup={'cancel','recover','finalize_cancel','stop_evidence','reconcile','scheduling_stop','settle','worker_failure'}
        if action not in cleanup:self._response_authority(c,snapshot)
        return (dict(j), snapshot, manifest, dict(q))

    def _response_authority(self,c,snapshot):
        for key in ('authority_guard','case_guard'):
            enabled=c.execute(select(t.guards.c.eligible).where(t.guards.c.key==snapshot[key])).scalar_one()
            if not enabled:raise Rejected('access_denied')

    def _op(self, c, p, resource, kind, key, body):
        if not isinstance(key, str) or not 0 < len(key) <= 256:
            raise Rejected('invalid_operation_key')
        data = canonical(body)
        row = c.execute(select(t.operations).where(t.operations.c.owner_ref == p.owner_ref, t.operations.c.resource_ref == str(resource), t.operations.c.kind == kind, t.operations.c.client_key == key)).mappings().first()
        if row:
            if row['canonical_schema'] != 'execution-command-v1' or bytes(row['canonical_command']) != data or bytes(row['command_sha256']) != digest(data):
                raise Conflict('operation_key_conflict')
            if row['outcome'] == 'rejected':
                raise Rejected(row['safe_reason'])
            return (row['response_refs'], data)
        return (None, data)

    def _finish(self, c, p, resource, kind, key, data, response, job=None, outcome='accepted', reason=None):
        oid = uuid4()
        c.execute(insert(t.operations).values(id=oid, owner_ref=p.owner_ref, resource_ref=str(resource), kind=kind, client_key=key, canonical_schema='execution-command-v1', canonical_command=data, command_sha256=digest(data), outcome=outcome, safe_reason=reason, response_refs=response, decided_at=func.clock_timestamp()))
        self._audit(c, p, kind, job, oid, **{'reason': reason} if reason else {})
        return oid

    def _run(self, p, job, kind, key, body, callback, *, heartbeat=False):
        try:
            return self.db.run(callback, heartbeat=heartbeat)
        except Rejected as exc:
            exc.audit_recorded = False
            if not heartbeat and exc.code not in {'commit_outcome_unknown', 'access_denied', 'authorizer_unavailable'}:
                try:

                    def record(c):
                        j, s, m, q = self._context(c, p, job, 'inspect', eligible=False)
                        try:old,data=self._op(c,p,job,kind,key,body)
                        except Conflict:
                            self._audit(c,p,'operation_conflict',job,command_digest=digest(canonical(body)).hex())
                            return
                        except Rejected:
                            self._audit(c,p,'rejected_operation_replay',job)
                            return
                        if old is None:
                            self._finish(c, p, job, kind, key, data, {}, job, 'rejected', exc.code)
                    self.db.run(record)
                    exc.audit_recorded = True
                except Exception:
                    pass
            raise

    def _pair(self, c, job_id):
        j = dict(c.execute(select(t.jobs).where(t.jobs.c.id == job_id)).mappings().one())
        a = [dict(x) for x in c.execute(select(t.attempts).where(t.attempts.c.job_id == job_id)).mappings()]
        q = dict(c.execute(select(t.queue_entries).where(t.queue_entries.c.job_id == job_id)).mappings().one())
        validate_pair(j, a, q)

    def _owned(self, c, j, lease):
        a = dict(c.execute(select(t.attempts).where(t.attempts.c.id == j['current_attempt_id']).with_for_update()).mappings().one())
        now = c.execute(select(func.clock_timestamp())).scalar_one()
        if j['id'] != lease.job_id or j['snapshot_id'] != lease.snapshot_id or j['version'] != lease.job_version or (j['state'] != 'running') or (a['state'] != 'running') or (a['id'] != lease.attempt_id) or (a['owner_instance'] != lease.owner_instance) or (a['fence'] != lease.fence) or (j['fence_counter'] != lease.fence) or (a['version'] != lease.attempt_version) or (a['lease_until'] is None) or (a['lease_until'] <= now):
            raise Rejected('stale_execution')
        return (a, now)

    def _lease(self, j, a):
        return Lease(j['id'], a['id'], a['owner_instance'], a['fence'], j['version'], a['version'], j['snapshot_id'])

    def get(self,p,job_id):
        def read(c):
            j,s,m,q=self._context(c,p,job_id,'inspect',eligible=False)
            return j
        return self.db.run(read)

    def submit(self, p, snapshot_id, key):
        body = {'snapshot_id': str(snapshot_id)}

        def run(c):
            c.execute(select(t.control).where(t.control.c.key == 'admission').with_for_update()).one()
            s = self._snapshot(c, snapshot_id)
            if s['owner_ref']!=p.owner_ref:raise Rejected('not_found')
            self.adapters.authorize(p, 'submit', s)
            self._guards(c,s,eligible=False)
            self._response_authority(c,s)
            old, data = self._op(c, p, s['case_ref'], 'submit', key, body)
            if old:
                return UUID(old['job_id'])
            self._guards(c,s)
            count = c.execute(select(func.count()).select_from(t.jobs).where(t.jobs.c.state.not_in(['succeeded', 'failed', 'cancelled']))).scalar_one()
            own = c.execute(select(func.count()).select_from(t.jobs).where(t.jobs.c.owner_ref == p.owner_ref, t.jobs.c.state.not_in(['succeeded', 'failed', 'cancelled']))).scalar_one()
            if count >= self.settings.global_admission or own >= self.settings.account_admission:
                raise CapacityUnavailable('admission_full')
            now = c.execute(select(func.clock_timestamp())).scalar_one()
            jid, aid = (uuid4(), uuid4())
            c.execute(pg_insert(t.dispatch_accounts).values(owner_ref=p.owner_ref, last_dispatch=0).on_conflict_do_nothing())
            c.execute(insert(t.jobs).values(id=jid, owner_ref=p.owner_ref, snapshot_id=snapshot_id, state='queued', version=1, attempt_count=1, max_attempts=self.settings.max_attempts, current_attempt_id=aid, created_at=now, updated_at=now))
            c.execute(insert(t.attempts).values(id=aid, job_id=jid, ordinal=1, state='pending', version=1, created_at=now))
            c.execute(insert(t.queue_entries).values(job_id=jid, owner_ref=p.owner_ref, pending_attempt_id=aid, enabled=True, ready_at=now, version=1))
            c.execute(insert(t.capacity_scopes).values(key='analysis_llm:' + str(jid), kind='analysis_llm', capacity=self.settings.analysis_llm_limit, in_use=0, version=1))
            self._pair(c, jid)
            self._finish(c, p, s['case_ref'], 'submit', key, data, {'job_id': str(jid)}, jid)
            return jid
        return self.db.run(run)

    def claim(self, p, instance):

        def run(c):
            control = c.execute(select(t.control).where(t.control.c.key == 'dispatch').with_for_update()).mappings().one()
            candidates = list(c.execute(select(t.dispatch_accounts).order_by(t.dispatch_accounts.c.last_dispatch, t.dispatch_accounts.c.owner_ref)).mappings())
            for account in candidates:
                head = c.execute(select(t.queue_entries).where(t.queue_entries.c.owner_ref == account['owner_ref'], t.queue_entries.c.enabled).order_by(t.queue_entries.c.submission_order).limit(1)).mappings().first()
                if not head:
                    continue
                q = c.execute(select(t.queue_entries).where(t.queue_entries.c.job_id == head['job_id'], t.queue_entries.c.enabled, t.queue_entries.c.ready_at <= func.clock_timestamp()).with_for_update(skip_locked=True)).mappings().first()
                if not q:
                    continue
                try:
                    j, s, m, q = self._context(c, p, q['job_id'], 'claim')
                except Rejected as exc:
                    if exc.code == 'access_denied':
                        continue
                    raise
                held = c.execute(select(t.reservations.c.id).where(t.reservations.c.job_id == j['id'], t.reservations.c.external_operation_id.is_(None), t.reservations.c.released_at.is_(None))).first()
                if held:
                    continue
                capacity.reserve(c, ['analyses'], j['id'], q['pending_attempt_id'], 'attempt:' + str(q['pending_attempt_id']))
                a = dict(c.execute(select(t.attempts).where(t.attempts.c.id == q['pending_attempt_id']).with_for_update()).mappings().one())
                if j['fence_counter'] >= MAX_COUNTER:
                    raise Rejected('fence_exhausted')
                allowed('J02' if j['state'] == 'queued' else 'J03', j['state'], 'running', 'dispatcher', a['state'], 'running')
                now = c.execute(select(func.clock_timestamp())).scalar_one()
                epoch = j['fence_counter'] + 1
                n = _checked(c, update(t.jobs).where(t.jobs.c.id == j['id'], t.jobs.c.version == j['version'], t.jobs.c.current_attempt_id == a['id']).values(state='running', fence_counter=epoch, version=j['version'] + 1, updated_at=now)).rowcount
                if n != 1:
                    raise Rejected('claim_conflict')
                _checked(c, update(t.attempts).where(t.attempts.c.id == a['id'], t.attempts.c.state == 'pending', t.attempts.c.version == a['version']).values(state='running', owner_instance=instance, fence=epoch, lease_until=now + timedelta(seconds=self.settings.lease_seconds), version=a['version'] + 1))
                _checked(c, update(t.queue_entries).where(t.queue_entries.c.job_id == j['id']).values(enabled=False, pending_attempt_id=None, version=t.queue_entries.c.version + 1))
                seq = control['sequence'] + 1
                if seq > MAX_COUNTER:
                    raise Rejected('dispatch_sequence_exhausted')
                _checked(c, update(t.control).where(t.control.c.key == 'dispatch').values(sequence=seq))
                _checked(c, update(t.dispatch_accounts).where(t.dispatch_accounts.c.owner_ref == j['owner_ref']).values(last_dispatch=seq))
                self._audit(c, p, 'claimed', j['id'], attempt=a['id'])
                self._pair(c, j['id'])
                j.update(state='running', version=j['version'] + 1, fence_counter=epoch)
                a.update(state='running', owner_instance=instance, fence=epoch, version=a['version'] + 1)
                return self._lease(j, a)
            return None
        return self.db.run(run)

    def current_lease(self,p,expected):
        """Reconnect only to the same live attempt/owner/fence, never whichever is latest."""
        def read(c):
            j,s,m,q=self._context(c,p,expected.job_id,'heartbeat')
            a=dict(c.execute(select(t.attempts).where(t.attempts.c.id==j['current_attempt_id'])).mappings().one())
            if (a['id']!=expected.attempt_id or a['owner_instance']!=expected.owner_instance
                or a['fence']!=expected.fence or j['snapshot_id']!=expected.snapshot_id):raise Rejected('stale_execution')
            current=self._lease(j,a)
            self._owned(c,j,current)
            return current
        return self.db.run(read,heartbeat=True)

    def heartbeat(self, p, lease, key):
        body = lease.command()

        def run(c):
            j, s, m, q = self._context(c, p, lease.job_id, 'heartbeat', eligible=False)
            old, data = self._op(c, p, j['id'], 'heartbeat', key, body)
            if old:
                return Lease.restore(old)
            self._guards(c, s)
            a, now = self._owned(c, j, lease)
            a['version'] += 1
            _checked(c, update(t.attempts).where(t.attempts.c.id == a['id'], t.attempts.c.version == lease.attempt_version, t.attempts.c.lease_until > now).values(version=a['version'], lease_until=now + timedelta(seconds=self.settings.lease_seconds)))
            result = self._lease(j, a)
            self._finish(c, p, j['id'], 'heartbeat', key, data, result.command(), j['id'])
            return result
        return self._run(p, lease.job_id, 'heartbeat', key, body, run, heartbeat=True)

    def publish(self, p, lease, key, payload, *, step=None, artifact_ids=(), reused_from=None, stop_proof=None):
        if not isinstance(payload, bytes) or not 0 < len(payload) <= 262144:
            raise Rejected('invalid_payload')
        kind = 'step' if step else 'final'
        body = {'lease': lease.command(), 'payload': payload.hex(), 'step': step, 'artifacts': [str(x) for x in artifact_ids], 'reused_from': str(reused_from) if reused_from else None, 'stop_proof': stop_proof.evidence_ref if stop_proof else None}
        body['payload'] = digest(payload).hex()

        def prepare(c):
            j, s, m, q = self._context(c, p, lease.job_id, 'publish', eligible=False)
            old, _ = self._op(c, p, j['id'], 'publish', key, body)
            if old:
                prior = c.execute(select(t.publications.c.payload).where(t.publications.c.id == UUID(old['publication_id']))).scalar_one()
                if bytes(prior) != payload:
                    raise Conflict('payload_conflict')
                return (UUID(old['publication_id']), None, [])
            artifacts = []
            for aid in artifact_ids:
                row = c.execute(select(t.artifacts).where(t.artifacts.c.id == aid, t.artifacts.c.owner_ref == p.owner_ref)).mappings().first()
                if not row:
                    raise Rejected('artifact_not_found')
                guard = c.execute(select(t.guards).where(t.guards.c.key == row['guard_key'])).mappings().one()
                artifacts.append((dict(row), dict(guard)))
            return (None, s, artifacts)
        replay, prepared, prepared_artifacts = self._run(p, lease.job_id, 'publish', key, body, prepare)
        if replay:
            return replay
        if self.adapters.validator is None:
            raise IntegrationUnavailable('validator_unavailable')
        try:binding=self.adapters.validator.validate(payload,prepared,kind)
        except Rejected:raise
        except Exception:raise Rejected('validation_failed') from None
        if not isinstance(binding, bytes) or len(binding) != 32:
            raise Rejected('invalid_validation_binding')
        for artifact, guard in prepared_artifacts:
            if self.adapters.artifacts is None:
                raise IntegrationUnavailable('artifact_unavailable')
            if not self.adapters.artifacts.ready(artifact, prepared):
                raise Rejected('artifact_not_ready')

        def run(c):
            j, s, m, q = self._context(c, p, lease.job_id, 'publish', eligible=False)
            old, data = self._op(c, p, j['id'], 'publish', key, body)
            if old:
                return UUID(old['publication_id'])
            self._guards(c, s)
            if bytes(s['manifest_sha256']) != bytes(prepared['manifest_sha256']):
                raise Rejected('prepared_snapshot_changed')
            artifacts = []
            for r, expected in sorted(prepared_artifacts, key=lambda pair: pair[0]['guard_key']):
                g = c.execute(select(t.guards).where(t.guards.c.key == r['guard_key']).with_for_update()).mappings().one()
                if g['kind'] != 'artifact' or not g['eligible'] or g['version'] != expected['version'] or (bytes(g['binding_sha256']) != bytes(expected['binding_sha256'])) or (bytes(g['binding_sha256']) != bytes(r['sha256'])) or (g['owner_ref'] not in {None, p.owner_ref}):
                    raise Rejected('artifact_not_ready')
                artifacts.append(r)
            scopekeys = [x[0] for x in c.execute(select(t.reservations.c.scope_key).where(t.reservations.c.job_id == j['id'], t.reservations.c.released_at.is_(None)))]
            capacity.lock_scopes(c, scopekeys)
            a, now = self._owned(c, j, lease)
            if not step and c.execute(select(t.external_operations.c.id).where(t.external_operations.c.job_id == j['id'], t.external_operations.c.settlement == 'unresolved')).first():
                raise Rejected('external_unsettled')
            if reused_from:
                source = c.execute(select(t.steps).where(t.steps.c.id == reused_from, t.steps.c.job_id == j['id'], t.steps.c.logical_key == step)).mappings().first()
                if not source or source['attempt_id'] == a['id'] or bytes(source['input_binding']) != bytes(s['manifest_sha256']):
                    raise Rejected('reuse_dependency')
            pid = uuid4()
            oid = self._finish(c, p, j['id'], 'publish', key, data, {'publication_id': str(pid)}, j['id'])
            c.execute(insert(t.publications).values(id=pid, job_id=j['id'], owner_ref=p.owner_ref, attempt_id=a['id'], kind=kind, logical_key=step or 'final', revision=1, operation_id=oid, payload_schema=m['output_schema'], payload=payload, payload_sha256=digest(payload), validation_binding=binding, accepted_at=now))
            for r in artifacts:
                c.execute(insert(t.publication_artifacts).values(publication_id=pid, artifact_id=r['id'], owner_ref=p.owner_ref))
            if step:
                c.execute(insert(t.steps).values(id=uuid4(), job_id=j['id'], attempt_id=a['id'], logical_key=step, input_binding=s['manifest_sha256'], publication_id=pid, reused_from=reused_from, completed_at=now))
            else:
                allowed('J04', j['state'], 'succeeded', 'worker', a['state'], 'succeeded')
                n = _checked(c, update(t.jobs).where(t.jobs.c.id == j['id'], t.jobs.c.version == lease.job_version, t.jobs.c.state == 'running', t.jobs.c.current_attempt_id == a['id'], t.jobs.c.fence_counter == lease.fence, t.jobs.c.snapshot_id == lease.snapshot_id).values(state='succeeded', final_publication_id=pid, version=j['version'] + 1, updated_at=now)).rowcount
                if n != 1:
                    raise Rejected('publication_conflict')
                _checked(c, update(t.attempts).where(t.attempts.c.id == a['id'], t.attempts.c.version == lease.attempt_version).values(state='succeeded', lease_until=None, ended_at=now, version=a['version'] + 1))
                if stop_proof is not None:
                    if self.adapters.stop is None or stop_proof.instance != a['owner_instance'] or (not self.adapters.stop.stopped(stop_proof, a)):
                        raise Rejected('stop_proof_invalid')
                    capacity.release(c, j['id'], a['id'], stop_proof.evidence_ref, analyses_only=True)
            self._pair(c, j['id'])
            return pid
        return self._run(p, lease.job_id, 'publish', key, body, run)

    def cancel(self, p, job_id, key, *, expected_version):
        body = {'expected_version': expected_version}

        def run(c):
            j, s, m, q = self._context(c, p, job_id, 'cancel', eligible=False)
            old, data = self._op(c, p, job_id, 'cancel', key, body)
            if old:
                return old['state']
            if j['version'] != expected_version:
                raise Rejected('stale_revision')
            a = c.execute(select(t.attempts).where(t.attempts.c.id == j['current_attempt_id']).with_for_update()).mappings().one()
            edge = {'queued': 'J13', 'retry_wait': 'J14', 'reconciliation_required': 'J15', 'running': 'J16'}.get(j['state'])
            if not edge:
                raise Rejected('invalid_transition')
            target = 'cancellation_requested' if j['state'] == 'running' else 'cancelled'
            atarget = target if edge != 'J15' else None
            allowed(edge, j['state'], target, 'cancellation', a['state'] if atarget else None, atarget)
            now = c.execute(select(func.clock_timestamp())).scalar_one()
            if atarget:
                _checked(c, update(t.attempts).where(t.attempts.c.id == a['id']).values(state=atarget, lease_until=None, ended_at=now if atarget == 'cancelled' else None, version=a['version'] + 1))
            _checked(c, update(t.jobs).where(t.jobs.c.id == job_id, t.jobs.c.version == expected_version).values(state=target, version=j['version'] + 1, updated_at=now))
            _checked(c, update(t.queue_entries).where(t.queue_entries.c.job_id == job_id).values(enabled=False, pending_attempt_id=None, version=t.queue_entries.c.version + 1))
            self._finish(c, p, job_id, 'cancel', key, data, {'state': target}, job_id)
            self._pair(c, job_id)
            return target
        return self._run(p, job_id, 'cancel', key, body, run)

def _checked(c,statement):
    result=c.execute(statement)
    if result.rowcount!=1:raise Rejected('conditional_write_rejected')
    return result
