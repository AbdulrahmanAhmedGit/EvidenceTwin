"""Static, centralized Core metadata. Importing never creates schema."""
from sqlalchemy import (MetaData, Table, Column, PrimaryKeyConstraint, UniqueConstraint, CheckConstraint, ForeignKeyConstraint, Index, Identity, text, Text)
from sqlalchemy.dialects.postgresql import UUID, TEXT, BIGINT, BOOLEAN, BYTEA, TIMESTAMP, INTEGER, JSONB
metadata=MetaData(schema="et_execution")

artifacts=Table('artifacts',metadata,
    Column('id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('guard_key',TEXT(),nullable=False),
    Column('object_ref',TEXT(),nullable=False),
    Column('object_version',TEXT(),nullable=False),
    Column('sha256',BYTEA(),nullable=False),
    Column('byte_count',BIGINT(),nullable=False),
    Column('media_type',TEXT(),nullable=False),
    Column('created_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint('byte_count >= 0',name='artifacts_byte_count_check'),
    PrimaryKeyConstraint('id',name='artifacts_pkey'),
    CheckConstraint('octet_length(sha256) = 32',name='artifacts_sha256_check'),
    UniqueConstraint('id','owner_ref',name='uq_artifact_owner'),
    UniqueConstraint('owner_ref','object_ref','object_version',name='uq_artifact_version'),
)

attempts=Table('attempts',metadata,
    Column('id',UUID(),nullable=False),
    Column('job_id',UUID(),nullable=False),
    Column('ordinal',INTEGER(),nullable=False),
    Column('state',TEXT(),nullable=False),
    Column('version',BIGINT(),nullable=False),
    Column('owner_instance',UUID(),nullable=True),
    Column('fence',BIGINT(),nullable=True),
    Column('lease_until',TIMESTAMP(timezone=True),nullable=True),
    Column('failure_code',TEXT(),nullable=True),
    Column('created_at',TIMESTAMP(timezone=True),nullable=False),
    Column('ended_at',TIMESTAMP(timezone=True),nullable=True),
    CheckConstraint('fence > 0',name='attempts_fence_check'),
    CheckConstraint('ordinal > 0',name='attempts_ordinal_check'),
    PrimaryKeyConstraint('id',name='attempts_pkey'),
    CheckConstraint("state = ANY (ARRAY['pending'::text, 'running'::text, 'cancellation_requested'::text, 'succeeded'::text, 'failed'::text, 'abandoned'::text, 'cancelled'::text])",name='attempts_state_check'),
    CheckConstraint('version > 0',name='attempts_version_check'),
    CheckConstraint("(state = ANY (ARRAY['succeeded'::text, 'failed'::text, 'abandoned'::text, 'cancelled'::text])) = (ended_at IS NOT NULL)",name='ck_attempt_end'),
    CheckConstraint("(state = 'running'::text) = (lease_until IS NOT NULL)",name='ck_attempt_lease'),
    CheckConstraint('(owner_instance IS NULL) = (fence IS NULL)',name='ck_attempt_owner_pair'),
    CheckConstraint("state <> 'pending'::text OR owner_instance IS NULL AND fence IS NULL",name='ck_attempt_pending_owner'),
    CheckConstraint("state <> 'running'::text OR owner_instance IS NOT NULL AND fence IS NOT NULL",name='ck_attempt_running_owner'),
    UniqueConstraint('job_id','id',name='uq_attempt_job_id'),
    UniqueConstraint('job_id','ordinal',name='uq_attempt_ordinal'),
)

audit_events=Table('audit_events',metadata,
    Column('id',UUID(),nullable=False),
    Column('job_id',UUID(),nullable=True),
    Column('operation_id',UUID(),nullable=True),
    Column('attempt_id',UUID(),nullable=True),
    Column('actor_ref',TEXT(),nullable=False),
    Column('event_type',TEXT(),nullable=False),
    Column('safe_metadata',JSONB(astext_type=Text()),nullable=False),
    Column('correlation_ref',UUID(),nullable=False),
    Column('occurred_at',TIMESTAMP(timezone=True),nullable=False),
    PrimaryKeyConstraint('id',name='audit_events_pkey'),
    CheckConstraint('attempt_id IS NULL OR job_id IS NOT NULL',name='ck_audit_attempt_job'),
)

capacity_scopes=Table('capacity_scopes',metadata,
    Column('key',TEXT(),nullable=False),
    Column('kind',TEXT(),nullable=False),
    Column('capacity',INTEGER(),nullable=False),
    Column('in_use',INTEGER(),nullable=False),
    Column('version',BIGINT(),nullable=False),
    CheckConstraint('capacity >= 0',name='capacity_scopes_capacity_check'),
    CheckConstraint('in_use >= 0 AND in_use <= capacity',name='capacity_scopes_check'),
    CheckConstraint("kind = ANY (ARRAY['analyses'::text, 'analysis_llm'::text, 'global_llm'::text, 'provider_llm'::text])",name='capacity_scopes_kind_check'),
    PrimaryKeyConstraint('key',name='capacity_scopes_pkey'),
    CheckConstraint('version > 0',name='capacity_scopes_version_check'),
)

control=Table('control',metadata,
    Column('key',TEXT(),nullable=False),
    Column('sequence',BIGINT(),server_default=text('0'),nullable=False),
    CheckConstraint("key = ANY (ARRAY['admission'::text, 'dispatch'::text])",name='control_key_check'),
    PrimaryKeyConstraint('key',name='control_pkey'),
    CheckConstraint('sequence >= 0',name='control_sequence_check'),
)

dispatch_accounts=Table('dispatch_accounts',metadata,
    Column('owner_ref',TEXT(),nullable=False),
    Column('last_dispatch',BIGINT(),server_default=text('0'),nullable=False),
    CheckConstraint('last_dispatch >= 0',name='dispatch_accounts_last_dispatch_check'),
    PrimaryKeyConstraint('owner_ref',name='dispatch_accounts_pkey'),
)

external_operations=Table('external_operations',metadata,
    Column('id',UUID(),nullable=False),
    Column('job_id',UUID(),nullable=False),
    Column('attempt_id',UUID(),nullable=False),
    Column('fence',BIGINT(),nullable=False),
    Column('logical_key',TEXT(),nullable=False),
    Column('step_key',TEXT(),nullable=False),
    Column('provider_configuration_ref',TEXT(),nullable=False),
    Column('request_ref',TEXT(),nullable=True),
    Column('settlement',TEXT(),nullable=False),
    Column('dispatch_intent_at',TIMESTAMP(timezone=True),nullable=False),
    Column('observed_at',TIMESTAMP(timezone=True),nullable=True),
    Column('version',BIGINT(),nullable=False),
    CheckConstraint('fence > 0',name='external_operations_fence_check'),
    PrimaryKeyConstraint('id',name='external_operations_pkey'),
    CheckConstraint("settlement = ANY (ARRAY['unresolved'::text, 'not_sent'::text, 'completed'::text, 'failed'::text])",name='external_operations_settlement_check'),
    CheckConstraint('version > 0',name='external_operations_version_check'),
    UniqueConstraint('job_id','attempt_id','id',name='uq_external_attempt_id'),
    UniqueConstraint('job_id','logical_key',name='uq_external_logical'),
)

guards=Table('guards',metadata,
    Column('key',TEXT(),nullable=False),
    Column('kind',TEXT(),nullable=False),
    Column('owner_ref',TEXT(),nullable=True),
    Column('version',BIGINT(),nullable=False),
    Column('eligible',BOOLEAN(),nullable=False),
    Column('binding_sha256',BYTEA(),nullable=False),
    CheckConstraint('octet_length(binding_sha256) = 32',name='guards_binding_sha256_check'),
    CheckConstraint("kind = ANY (ARRAY['authority'::text, 'case'::text, 'snapshot'::text, 'policy'::text, 'configuration'::text, 'artifact'::text])",name='guards_kind_check'),
    PrimaryKeyConstraint('key',name='guards_pkey'),
    CheckConstraint('version > 0',name='guards_version_check'),
)

jobs=Table('jobs',metadata,
    Column('id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('snapshot_id',UUID(),nullable=False),
    Column('state',TEXT(),nullable=False),
    Column('version',BIGINT(),nullable=False),
    Column('fence_counter',BIGINT(),server_default=text('0'),nullable=False),
    Column('attempt_count',INTEGER(),nullable=False),
    Column('max_attempts',INTEGER(),nullable=False),
    Column('current_attempt_id',UUID(),nullable=False),
    Column('final_publication_id',UUID(),nullable=True),
    Column('failure_code',TEXT(),nullable=True),
    Column('created_at',TIMESTAMP(timezone=True),nullable=False),
    Column('updated_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint("(state = 'succeeded'::text) = (final_publication_id IS NOT NULL)",name='ck_job_final'),
    CheckConstraint('attempt_count > 0',name='jobs_attempt_count_check'),
    CheckConstraint('max_attempts > 0 AND attempt_count <= max_attempts',name='jobs_check'),
    CheckConstraint('fence_counter >= 0',name='jobs_fence_counter_check'),
    PrimaryKeyConstraint('id',name='jobs_pkey'),
    CheckConstraint("state = ANY (ARRAY['queued'::text, 'running'::text, 'retry_wait'::text, 'reconciliation_required'::text, 'cancellation_requested'::text, 'succeeded'::text, 'failed'::text, 'cancelled'::text])",name='jobs_state_check'),
    CheckConstraint('version > 0',name='jobs_version_check'),
    UniqueConstraint('id','owner_ref',name='uq_job_owner'),
)

operations=Table('operations',metadata,
    Column('id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('resource_ref',TEXT(),nullable=False),
    Column('kind',TEXT(),nullable=False),
    Column('client_key',TEXT(),nullable=False),
    Column('canonical_schema',TEXT(),nullable=False),
    Column('canonical_command',BYTEA(),nullable=False),
    Column('command_sha256',BYTEA(),nullable=False),
    Column('outcome',TEXT(),nullable=False),
    Column('safe_reason',TEXT(),nullable=True),
    Column('response_refs',JSONB(astext_type=Text()),nullable=False),
    Column('decided_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint('octet_length(canonical_command) >= 1 AND octet_length(canonical_command) <= 262144',name='operations_canonical_command_check'),
    CheckConstraint('length(client_key) >= 1 AND length(client_key) <= 256',name='operations_client_key_check'),
    CheckConstraint('octet_length(command_sha256) = 32',name='operations_command_sha256_check'),
    CheckConstraint("outcome = ANY (ARRAY['accepted'::text, 'rejected'::text])",name='operations_outcome_check'),
    PrimaryKeyConstraint('id',name='operations_pkey'),
    UniqueConstraint('owner_ref','resource_ref','kind','client_key',name='uq_operation_scope'),
)

publication_artifacts=Table('publication_artifacts',metadata,
    Column('publication_id',UUID(),nullable=False),
    Column('artifact_id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    PrimaryKeyConstraint('publication_id','artifact_id',name='publication_artifacts_pkey'),
)

publications=Table('publications',metadata,
    Column('id',UUID(),nullable=False),
    Column('job_id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('attempt_id',UUID(),nullable=False),
    Column('kind',TEXT(),nullable=False),
    Column('logical_key',TEXT(),nullable=False),
    Column('revision',BIGINT(),nullable=False),
    Column('predecessor_id',UUID(),nullable=True),
    Column('operation_id',UUID(),nullable=False),
    Column('payload_schema',TEXT(),nullable=False),
    Column('payload',BYTEA(),nullable=False),
    Column('payload_sha256',BYTEA(),nullable=False),
    Column('validation_binding',BYTEA(),nullable=False),
    Column('accepted_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint("kind = ANY (ARRAY['step'::text, 'final'::text])",name='publications_kind_check'),
    UniqueConstraint('operation_id',name='publications_operation_id_key'),
    CheckConstraint('octet_length(payload) >= 1 AND octet_length(payload) <= 262144',name='publications_payload_check'),
    CheckConstraint('octet_length(payload_sha256) = 32',name='publications_payload_sha256_check'),
    PrimaryKeyConstraint('id',name='publications_pkey'),
    CheckConstraint('revision > 0',name='publications_revision_check'),
    CheckConstraint('octet_length(validation_binding) = 32',name='publications_validation_binding_check'),
    UniqueConstraint('job_id','attempt_id','id',name='uq_publication_attempt_id'),
    UniqueConstraint('job_id','id',name='uq_publication_job_id'),
    UniqueConstraint('id','owner_ref',name='uq_publication_owner'),
    UniqueConstraint('job_id','attempt_id','kind','logical_key','revision',name='uq_publication_revision'),
)

queue_entries=Table('queue_entries',metadata,
    Column('job_id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('pending_attempt_id',UUID(),nullable=True),
    Column('enabled',BOOLEAN(),nullable=False),
    Column('ready_at',TIMESTAMP(timezone=True),nullable=False),
    Column('submission_order',BIGINT(),Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1),nullable=False),
    Column('version',BIGINT(),nullable=False),
    CheckConstraint('enabled = (pending_attempt_id IS NOT NULL)',name='ck_queue_pending'),
    PrimaryKeyConstraint('job_id',name='queue_entries_pkey'),
    UniqueConstraint('submission_order',name='queue_entries_submission_order_key'),
    CheckConstraint('version > 0',name='queue_entries_version_check'),
)

reservations=Table('reservations',metadata,
    Column('id',UUID(),nullable=False),
    Column('scope_key',TEXT(),nullable=False),
    Column('job_id',UUID(),nullable=False),
    Column('attempt_id',UUID(),nullable=False),
    Column('external_operation_id',UUID(),nullable=True),
    Column('logical_key',TEXT(),nullable=False),
    Column('reserved_at',TIMESTAMP(timezone=True),nullable=False),
    Column('released_at',TIMESTAMP(timezone=True),nullable=True),
    Column('release_proof_ref',TEXT(),nullable=True),
    CheckConstraint('(released_at IS NULL) = (release_proof_ref IS NULL)',name='ck_release_proof'),
    PrimaryKeyConstraint('id',name='reservations_pkey'),
)

snapshots=Table('snapshots',metadata,
    Column('id',UUID(),nullable=False),
    Column('owner_ref',TEXT(),nullable=False),
    Column('case_ref',TEXT(),nullable=False),
    Column('analysis_ref',TEXT(),nullable=False),
    Column('analysis_revision',TEXT(),nullable=False),
    Column('authority_guard',TEXT(),nullable=False),
    Column('case_guard',TEXT(),nullable=False),
    Column('evidence_guard',TEXT(),nullable=False),
    Column('policy_guard',TEXT(),nullable=False),
    Column('configuration_guard',TEXT(),nullable=False),
    Column('schema_ref',TEXT(),nullable=False),
    Column('manifest',BYTEA(),nullable=False),
    Column('manifest_sha256',BYTEA(),nullable=False),
    Column('created_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint('octet_length(manifest) >= 1 AND octet_length(manifest) <= 262144',name='snapshots_manifest_check'),
    CheckConstraint('octet_length(manifest_sha256) = 32',name='snapshots_manifest_sha256_check'),
    PrimaryKeyConstraint('id',name='snapshots_pkey'),
    UniqueConstraint('id','owner_ref',name='uq_snapshot_owner'),
)

steps=Table('steps',metadata,
    Column('id',UUID(),nullable=False),
    Column('job_id',UUID(),nullable=False),
    Column('attempt_id',UUID(),nullable=False),
    Column('logical_key',TEXT(),nullable=False),
    Column('input_binding',BYTEA(),nullable=False),
    Column('publication_id',UUID(),nullable=False),
    Column('reused_from',UUID(),nullable=True),
    Column('completed_at',TIMESTAMP(timezone=True),nullable=False),
    CheckConstraint('octet_length(input_binding) = 32',name='steps_input_binding_check'),
    PrimaryKeyConstraint('id',name='steps_pkey'),
    UniqueConstraint('job_id','attempt_id','logical_key',name='uq_step_attempt_key'),
    UniqueConstraint('job_id','id',name='uq_step_job_id'),
)

artifacts.append_constraint(ForeignKeyConstraint(['guard_key'],['et_execution.guards.key'],name='artifacts_guard_key_fkey',deferrable=None,initially=None))
attempts.append_constraint(ForeignKeyConstraint(['job_id'],['et_execution.jobs.id'],name='attempts_job_id_fkey',deferrable=None,initially=None))
audit_events.append_constraint(ForeignKeyConstraint(['job_id'],['et_execution.jobs.id'],name='audit_events_job_id_fkey',deferrable=None,initially=None))
audit_events.append_constraint(ForeignKeyConstraint(['operation_id'],['et_execution.operations.id'],name='audit_events_operation_id_fkey',deferrable=None,initially=None))
audit_events.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_audit_attempt',deferrable=None,initially=None))
external_operations.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_external_attempt',deferrable=None,initially=None))
jobs.append_constraint(ForeignKeyConstraint(['id', 'current_attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_job_current_attempt',deferrable=True,initially='DEFERRED'))
jobs.append_constraint(ForeignKeyConstraint(['id', 'final_publication_id'],['et_execution.publications.job_id', 'et_execution.publications.id'],name='fk_job_final_publication',deferrable=True,initially='DEFERRED'))
jobs.append_constraint(ForeignKeyConstraint(['snapshot_id', 'owner_ref'],['et_execution.snapshots.id', 'et_execution.snapshots.owner_ref'],name='fk_job_snapshot_owner',deferrable=None,initially=None))
jobs.append_constraint(ForeignKeyConstraint(['owner_ref'],['et_execution.dispatch_accounts.owner_ref'],name='jobs_owner_ref_fkey',deferrable=None,initially=None))
publication_artifacts.append_constraint(ForeignKeyConstraint(['artifact_id', 'owner_ref'],['et_execution.artifacts.id', 'et_execution.artifacts.owner_ref'],name='fk_accepted_artifact_owner',deferrable=None,initially=None))
publication_artifacts.append_constraint(ForeignKeyConstraint(['publication_id', 'owner_ref'],['et_execution.publications.id', 'et_execution.publications.owner_ref'],name='fk_accepted_publication_owner',deferrable=None,initially=None))
publications.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_publication_attempt',deferrable=None,initially=None))
publications.append_constraint(ForeignKeyConstraint(['job_id', 'owner_ref'],['et_execution.jobs.id', 'et_execution.jobs.owner_ref'],name='fk_publication_owner',deferrable=None,initially=None))
publications.append_constraint(ForeignKeyConstraint(['job_id', 'predecessor_id'],['et_execution.publications.job_id', 'et_execution.publications.id'],name='fk_publication_predecessor',deferrable=None,initially=None))
publications.append_constraint(ForeignKeyConstraint(['operation_id'],['et_execution.operations.id'],name='publications_operation_id_fkey',deferrable=None,initially=None))
queue_entries.append_constraint(ForeignKeyConstraint(['job_id', 'pending_attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_queue_attempt',deferrable=None,initially=None))
queue_entries.append_constraint(ForeignKeyConstraint(['job_id', 'owner_ref'],['et_execution.jobs.id', 'et_execution.jobs.owner_ref'],name='fk_queue_job_owner',deferrable=None,initially=None))
reservations.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_reservation_attempt',deferrable=None,initially=None))
reservations.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id', 'external_operation_id'],['et_execution.external_operations.job_id', 'et_execution.external_operations.attempt_id', 'et_execution.external_operations.id'],name='fk_reservation_external',deferrable=None,initially=None))
reservations.append_constraint(ForeignKeyConstraint(['scope_key'],['et_execution.capacity_scopes.key'],name='reservations_scope_key_fkey',deferrable=None,initially=None))
snapshots.append_constraint(ForeignKeyConstraint(['authority_guard'],['et_execution.guards.key'],name='snapshots_authority_guard_fkey',deferrable=None,initially=None))
snapshots.append_constraint(ForeignKeyConstraint(['case_guard'],['et_execution.guards.key'],name='snapshots_case_guard_fkey',deferrable=None,initially=None))
snapshots.append_constraint(ForeignKeyConstraint(['configuration_guard'],['et_execution.guards.key'],name='snapshots_configuration_guard_fkey',deferrable=None,initially=None))
snapshots.append_constraint(ForeignKeyConstraint(['evidence_guard'],['et_execution.guards.key'],name='snapshots_evidence_guard_fkey',deferrable=None,initially=None))
snapshots.append_constraint(ForeignKeyConstraint(['policy_guard'],['et_execution.guards.key'],name='snapshots_policy_guard_fkey',deferrable=None,initially=None))
steps.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id'],['et_execution.attempts.job_id', 'et_execution.attempts.id'],name='fk_step_attempt',deferrable=None,initially=None))
steps.append_constraint(ForeignKeyConstraint(['job_id', 'attempt_id', 'publication_id'],['et_execution.publications.job_id', 'et_execution.publications.attempt_id', 'et_execution.publications.id'],name='fk_step_publication',deferrable=None,initially=None))
steps.append_constraint(ForeignKeyConstraint(['job_id', 'reused_from'],['et_execution.steps.job_id', 'et_execution.steps.id'],name='fk_step_reused',deferrable=None,initially=None))
Index('ix_attempt_lease',attempts.c.lease_until,attempts.c.job_id,unique=False,postgresql_where=text("(state = 'running'::text)"))
Index('uq_attempt_executable',attempts.c.job_id,unique=True,postgresql_where=text("(state = ANY (ARRAY['pending'::text, 'running'::text, 'cancellation_requested'::text]))"))
Index('ix_audit_job_time',audit_events.c.job_id,audit_events.c.occurred_at,audit_events.c.id,unique=False)
Index('ix_audit_operation',audit_events.c.operation_id,unique=False)
Index('ix_external_unsettled',external_operations.c.job_id,unique=False,postgresql_where=text("(settlement = 'unresolved'::text)"))
Index('ix_job_owner_state',jobs.c.owner_ref,jobs.c.state,jobs.c.created_at,jobs.c.id,unique=False)
Index('ix_publication_attempt',publications.c.attempt_id,unique=False)
Index('uq_publication_final',publications.c.job_id,unique=True,postgresql_where=text("(kind = 'final'::text)"))
Index('ix_queue_ready',queue_entries.c.owner_ref,queue_entries.c.submission_order,queue_entries.c.ready_at,unique=False,postgresql_where=text('enabled'))
Index('ix_reservation_external',reservations.c.external_operation_id,unique=False)
Index('ix_reservation_job',reservations.c.job_id,reservations.c.attempt_id,unique=False,postgresql_where=text('(released_at IS NULL)'))
Index('uq_reservation_live',reservations.c.scope_key,reservations.c.logical_key,unique=True,postgresql_where=text('(released_at IS NULL)'))
Index('ix_step_publication',steps.c.publication_id,unique=False)
