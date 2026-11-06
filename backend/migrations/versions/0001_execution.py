"""Reviewed immutable execution schema; no scientific implementation.

Revision: 0001_execution. Only explicit Alembic invocation creates schema.
"""
from alembic import op
revision = '0001_execution'
down_revision = None
branch_labels = None
depends_on = None
DDL = """
CREATE TABLE control (
  key text PRIMARY KEY CHECK (key IN ('admission','dispatch')),
  sequence bigint NOT NULL DEFAULT 0 CHECK (sequence >= 0)
);
CREATE TABLE dispatch_accounts (
  owner_ref text PRIMARY KEY,
  last_dispatch bigint NOT NULL DEFAULT 0 CHECK (last_dispatch >= 0)
);
CREATE TABLE guards (
  key text PRIMARY KEY,
  kind text NOT NULL CHECK (kind IN ('authority','case','snapshot','policy','configuration','artifact')),
  owner_ref text,
  version bigint NOT NULL CHECK (version > 0),
  eligible boolean NOT NULL,
  binding_sha256 bytea NOT NULL CHECK (octet_length(binding_sha256)=32)
);
CREATE TABLE snapshots (
  id uuid PRIMARY KEY,
  owner_ref text NOT NULL,
  case_ref text NOT NULL,
  analysis_ref text NOT NULL,
  analysis_revision text NOT NULL,
  authority_guard text NOT NULL REFERENCES guards(key),
  case_guard text NOT NULL REFERENCES guards(key),
  evidence_guard text NOT NULL REFERENCES guards(key),
  policy_guard text NOT NULL REFERENCES guards(key),
  configuration_guard text NOT NULL REFERENCES guards(key),
  schema_ref text NOT NULL,
  manifest bytea NOT NULL CHECK (octet_length(manifest) BETWEEN 1 AND 262144),
  manifest_sha256 bytea NOT NULL CHECK (octet_length(manifest_sha256)=32),
  created_at timestamptz NOT NULL,
  CONSTRAINT uq_snapshot_owner UNIQUE(id,owner_ref)
);
CREATE TABLE jobs (
  id uuid PRIMARY KEY,
  owner_ref text NOT NULL REFERENCES dispatch_accounts(owner_ref),
  snapshot_id uuid NOT NULL,
  state text NOT NULL CHECK (state IN ('queued','running','retry_wait','reconciliation_required',
    'cancellation_requested','succeeded','failed','cancelled')),
  version bigint NOT NULL CHECK (version > 0),
  fence_counter bigint NOT NULL DEFAULT 0 CHECK (fence_counter >= 0),
  attempt_count integer NOT NULL CHECK (attempt_count > 0),
  max_attempts integer NOT NULL CHECK (max_attempts > 0 AND attempt_count <= max_attempts),
  current_attempt_id uuid NOT NULL,
  final_publication_id uuid,
  failure_code text,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  CONSTRAINT uq_job_owner UNIQUE(id,owner_ref),
  CONSTRAINT fk_job_snapshot_owner FOREIGN KEY(snapshot_id,owner_ref) REFERENCES snapshots(id,owner_ref),
  CONSTRAINT ck_job_final CHECK ((state='succeeded')=(final_publication_id IS NOT NULL))
);
CREATE TABLE attempts (
  id uuid PRIMARY KEY,
  job_id uuid NOT NULL REFERENCES jobs(id),
  ordinal integer NOT NULL CHECK (ordinal > 0),
  state text NOT NULL CHECK (state IN ('pending','running','cancellation_requested','succeeded','failed','abandoned','cancelled')),
  version bigint NOT NULL CHECK (version > 0),
  owner_instance uuid,
  fence bigint CHECK (fence > 0),
  lease_until timestamptz,
  failure_code text,
  created_at timestamptz NOT NULL,
  ended_at timestamptz,
  CONSTRAINT uq_attempt_job_id UNIQUE(job_id,id),
  CONSTRAINT uq_attempt_ordinal UNIQUE(job_id,ordinal),
  CONSTRAINT ck_attempt_lease CHECK ((state='running')=(lease_until IS NOT NULL)),
  CONSTRAINT ck_attempt_running_owner CHECK (state<>'running' OR (owner_instance IS NOT NULL AND fence IS NOT NULL)),
  CONSTRAINT ck_attempt_owner_pair CHECK ((owner_instance IS NULL)=(fence IS NULL)),
  CONSTRAINT ck_attempt_pending_owner CHECK (state<>'pending' OR (owner_instance IS NULL AND fence IS NULL)),
  CONSTRAINT ck_attempt_end CHECK ((state IN ('succeeded','failed','abandoned','cancelled'))=(ended_at IS NOT NULL))
);
CREATE UNIQUE INDEX uq_attempt_executable ON attempts(job_id)
  WHERE state IN ('pending','running','cancellation_requested');
ALTER TABLE jobs ADD CONSTRAINT fk_job_current_attempt
  FOREIGN KEY(id,current_attempt_id) REFERENCES attempts(job_id,id) DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE queue_entries (
  job_id uuid PRIMARY KEY,
  owner_ref text NOT NULL,
  pending_attempt_id uuid,
  enabled boolean NOT NULL,
  ready_at timestamptz NOT NULL,
  submission_order bigint GENERATED ALWAYS AS IDENTITY UNIQUE,
  version bigint NOT NULL CHECK (version > 0),
  CONSTRAINT fk_queue_job_owner FOREIGN KEY(job_id,owner_ref) REFERENCES jobs(id,owner_ref),
  CONSTRAINT fk_queue_attempt FOREIGN KEY(job_id,pending_attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT ck_queue_pending CHECK (enabled=(pending_attempt_id IS NOT NULL))
);
CREATE INDEX ix_queue_ready ON queue_entries(owner_ref,submission_order,ready_at) WHERE enabled;
CREATE INDEX ix_job_owner_state ON jobs(owner_ref,state,created_at,id);
CREATE INDEX ix_attempt_lease ON attempts(lease_until,job_id) WHERE state='running';
CREATE TABLE operations (
  id uuid PRIMARY KEY,
  owner_ref text NOT NULL,
  resource_ref text NOT NULL,
  kind text NOT NULL,
  client_key text NOT NULL CHECK (length(client_key) BETWEEN 1 AND 256),
  canonical_schema text NOT NULL,
  canonical_command bytea NOT NULL CHECK (octet_length(canonical_command) BETWEEN 1 AND 262144),
  command_sha256 bytea NOT NULL CHECK (octet_length(command_sha256)=32),
  outcome text NOT NULL CHECK (outcome IN ('accepted','rejected')),
  safe_reason text,
  response_refs jsonb NOT NULL,
  decided_at timestamptz NOT NULL,
  CONSTRAINT uq_operation_scope UNIQUE(owner_ref,resource_ref,kind,client_key)
);
CREATE TABLE publications (
  id uuid PRIMARY KEY,
  job_id uuid NOT NULL,
  owner_ref text NOT NULL,
  attempt_id uuid NOT NULL,
  kind text NOT NULL CHECK (kind IN ('step','final')),
  logical_key text NOT NULL,
  revision bigint NOT NULL CHECK (revision > 0),
  predecessor_id uuid,
  operation_id uuid NOT NULL UNIQUE REFERENCES operations(id),
  payload_schema text NOT NULL,
  payload bytea NOT NULL CHECK (octet_length(payload) BETWEEN 1 AND 262144),
  payload_sha256 bytea NOT NULL CHECK (octet_length(payload_sha256)=32),
  validation_binding bytea NOT NULL CHECK (octet_length(validation_binding)=32),
  accepted_at timestamptz NOT NULL,
  CONSTRAINT fk_publication_owner FOREIGN KEY(job_id,owner_ref) REFERENCES jobs(id,owner_ref),
  CONSTRAINT fk_publication_attempt FOREIGN KEY(job_id,attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT uq_publication_revision UNIQUE(job_id,attempt_id,kind,logical_key,revision),
  CONSTRAINT uq_publication_job_id UNIQUE(job_id,id),
  CONSTRAINT uq_publication_attempt_id UNIQUE(job_id,attempt_id,id),
  CONSTRAINT fk_publication_predecessor FOREIGN KEY(job_id,predecessor_id) REFERENCES publications(job_id,id),
  CONSTRAINT uq_publication_owner UNIQUE(id,owner_ref)
);
CREATE UNIQUE INDEX uq_publication_final ON publications(job_id) WHERE kind='final';
ALTER TABLE jobs ADD CONSTRAINT fk_job_final_publication
  FOREIGN KEY(id,final_publication_id) REFERENCES publications(job_id,id) DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE steps (
  id uuid PRIMARY KEY,
  job_id uuid NOT NULL,
  attempt_id uuid NOT NULL,
  logical_key text NOT NULL,
  input_binding bytea NOT NULL CHECK (octet_length(input_binding)=32),
  publication_id uuid NOT NULL,
  reused_from uuid,
  completed_at timestamptz NOT NULL,
  CONSTRAINT fk_step_attempt FOREIGN KEY(job_id,attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT fk_step_publication FOREIGN KEY(job_id,attempt_id,publication_id) REFERENCES publications(job_id,attempt_id,id),
  CONSTRAINT uq_step_job_id UNIQUE(job_id,id),
  CONSTRAINT fk_step_reused FOREIGN KEY(job_id,reused_from) REFERENCES steps(job_id,id),
  CONSTRAINT uq_step_attempt_key UNIQUE(job_id,attempt_id,logical_key)
);
CREATE TABLE artifacts (
  id uuid PRIMARY KEY,
  owner_ref text NOT NULL,
  guard_key text NOT NULL REFERENCES guards(key),
  object_ref text NOT NULL,
  object_version text NOT NULL,
  sha256 bytea NOT NULL CHECK (octet_length(sha256)=32),
  byte_count bigint NOT NULL CHECK (byte_count >= 0),
  media_type text NOT NULL,
  created_at timestamptz NOT NULL,
  CONSTRAINT uq_artifact_owner UNIQUE(id,owner_ref),
  CONSTRAINT uq_artifact_version UNIQUE(owner_ref,object_ref,object_version)
);
CREATE TABLE publication_artifacts (
  publication_id uuid NOT NULL,
  artifact_id uuid NOT NULL,
  owner_ref text NOT NULL,
  PRIMARY KEY(publication_id,artifact_id),
  CONSTRAINT fk_accepted_publication_owner FOREIGN KEY(publication_id,owner_ref) REFERENCES publications(id,owner_ref),
  CONSTRAINT fk_accepted_artifact_owner FOREIGN KEY(artifact_id,owner_ref) REFERENCES artifacts(id,owner_ref)
);
CREATE TABLE capacity_scopes (
  key text PRIMARY KEY,
  kind text NOT NULL CHECK (kind IN ('analyses','analysis_llm','global_llm','provider_llm')),
  capacity integer NOT NULL CHECK (capacity >= 0),
  in_use integer NOT NULL CHECK (in_use >= 0 AND in_use <= capacity),
  version bigint NOT NULL CHECK (version > 0)
);
CREATE TABLE external_operations (
  id uuid PRIMARY KEY,
  job_id uuid NOT NULL,
  attempt_id uuid NOT NULL,
  fence bigint NOT NULL CHECK (fence > 0),
  logical_key text NOT NULL,
  step_key text NOT NULL,
  provider_configuration_ref text NOT NULL,
  request_ref text,
  settlement text NOT NULL CHECK (settlement IN ('unresolved','not_sent','completed','failed')),
  dispatch_intent_at timestamptz NOT NULL,
  observed_at timestamptz,
  version bigint NOT NULL CHECK (version > 0),
  CONSTRAINT fk_external_attempt FOREIGN KEY(job_id,attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT uq_external_logical UNIQUE(job_id,logical_key),
  CONSTRAINT uq_external_attempt_id UNIQUE(job_id,attempt_id,id)
);
CREATE TABLE reservations (
  id uuid PRIMARY KEY,
  scope_key text NOT NULL REFERENCES capacity_scopes(key),
  job_id uuid NOT NULL,
  attempt_id uuid NOT NULL,
  external_operation_id uuid,
  logical_key text NOT NULL,
  reserved_at timestamptz NOT NULL,
  released_at timestamptz,
  release_proof_ref text,
  CONSTRAINT fk_reservation_attempt FOREIGN KEY(job_id,attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT fk_reservation_external FOREIGN KEY(job_id,attempt_id,external_operation_id) REFERENCES external_operations(job_id,attempt_id,id),
  CONSTRAINT ck_release_proof CHECK ((released_at IS NULL)=(release_proof_ref IS NULL))
);
CREATE UNIQUE INDEX uq_reservation_live ON reservations(scope_key,logical_key) WHERE released_at IS NULL;
CREATE INDEX ix_reservation_job ON reservations(job_id,attempt_id) WHERE released_at IS NULL;
CREATE INDEX ix_external_unsettled ON external_operations(job_id) WHERE settlement='unresolved';
CREATE TABLE audit_events (
  id uuid PRIMARY KEY,
  job_id uuid REFERENCES jobs(id),
  operation_id uuid REFERENCES operations(id),
  attempt_id uuid,
  actor_ref text NOT NULL,
  event_type text NOT NULL,
  safe_metadata jsonb NOT NULL,
  correlation_ref uuid NOT NULL,
  occurred_at timestamptz NOT NULL,
  CONSTRAINT fk_audit_attempt FOREIGN KEY(job_id,attempt_id) REFERENCES attempts(job_id,id),
  CONSTRAINT ck_audit_attempt_job CHECK (attempt_id IS NULL OR job_id IS NOT NULL)
);
CREATE INDEX ix_audit_job_time ON audit_events(job_id,occurred_at,id);
CREATE INDEX ix_step_publication ON steps(publication_id);
CREATE INDEX ix_publication_attempt ON publications(attempt_id);
CREATE INDEX ix_reservation_external ON reservations(external_operation_id);
CREATE INDEX ix_audit_operation ON audit_events(operation_id);
"""

def upgrade():
    op.execute('CREATE SCHEMA et_execution')
    op.execute('SET LOCAL search_path TO et_execution, pg_catalog')
    for statement in DDL.split(';'):
        if statement.strip(): op.execute(statement)
    op.execute("INSERT INTO control(key) VALUES ('admission'),('dispatch')")

def downgrade():
    # env.py independently prohibits non-disposable databases.
    op.execute('DROP SCHEMA et_execution CASCADE')
