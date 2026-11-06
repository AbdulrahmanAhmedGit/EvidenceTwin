# EvidenceTwin V1 — Execution integration environment and acceptance specification

**Status: Recommended for owner approval.** Date: 2026-11-06. All **24 gates remain OPEN**. All test rows are unexecuted specifications. No test database, service, migration, task implementation or dependency has been created or run during this design preparation.

## 1. Recommended isolated test environment

Use a disposable local PostgreSQL **18.6** service, with the same major/minor for hosted testing until a reviewed patch update. Recommend an optional Compose profile in `backend/compose.execution-test.yaml`, created only after coding authorization. Do not require Docker for a researcher; this is developer test tooling. Use a matching externally provisioned disposable PostgreSQL when an engine is unavailable; never install/start Docker or a database implicitly in test collection.

The future profile binds only 127.0.0.1 on an ephemeral host port, uses a dedicated random test credential passed through a temporary mode-0600 environment/secret file, no real data directory mount, no production network and a disposable volume. Pin postgres:18.6 plus the actual retrieved immutable image digest at authorized provisioning; no digest is invented here. No remote/public exposure or hosted deployment is included. If no supported local tool exists, the implementation must report missing test infrastructure rather than change host services without authorization.

Use `ET_EXECUTION_TEST_ADMIN_DSN` exclusively for the fixture administrator connection. Never fall back to runtime DATABASE_URL, a discovered .env, standard postgres database, local instance data or provider credentials. Existing tests clear EVIDENCETWIN_* variables; the separate ET_EXECUTION_TEST_* namespace avoids accidental fixture erasure. Do not log the DSN. Explicit test opt-in and a database sentinel are both required before destructive setup/cleanup.

The fixture administrator creates a database named et_test_<random hex> and a least-privileged runtime role for each case or deliberately shared concurrent scenario. Validate the generated identifier against a strict literal prefix/hex allowlist and quote identifiers through the database API; values remain bound. Run only reviewed Alembic migrations as the fixture migration owner, then connect worker processes with DML-only credentials. No create_all. Each case uses fixed qualified schema et_execution inside its unique disposable database. Runtime code cannot create/drop databases, alter schema, truncate tables or access another test database.

Cleanup tracks exactly the fixture-created database/role/service identity; stop/join/reap children, revoke only its connections, then drop only recorded et_test_* databases/roles and disposable volumes. A failed cleanup produces an explicit report, never a broad DROP/volume prune. If supplied DSN lacks the test sentinel/expected server/permission shape, abort before migration. CI must fail required integration acceptance when PostgreSQL is unavailable; optional developer skips must remain clearly reported as missing evidence.

## 2. Process and failure harness

Use at least two independent Python worker processes against one test database, plus separate controller/observer connections. Build Engines inside each child after spawn. Test helpers/tasks/provider simulator live only under backend/tests/execution. Controlled task outputs explicitly identify themselves as test fixtures; there is no production sample-success executor.

Use barriers/events to arrange races and database observations to prove commits. Join with bounded deadlines and collect exit statuses. Clock-dependent expiry tests use server timestamps and deliberately short test-only configurations or reviewed fixture writes in disposable data; production never accepts a caller's fake clock. Jitter uses an injected deterministic test random source. Do not infer race correctness from sleep duration alone.

For crash tests, terminate the actual child process after observed durable checkpoints/dispatch intent. Verify the database via a new connection, then restart a separate worker. A simulated provider can hold a call after the worker dies; its release is an explicit test action. This proves modeled uncertainty handling, not real-provider exactly-once delivery or cancellation behavior.

## 3. Acceptance matrix — unexecuted

| ID | Scenario and arranged condition | Required observation |
| --- | --- | --- |
| EX01 | Fresh database migrations; metadata inspection | All 16 proposed tables and constraints/indexes exist; FK ordering succeeds; no runtime schema creation. |
| EX02 | Invalid row-local state/lease/end fields | Database rejects; no partial writes. |
| EX03 | Cross-job attempt/snapshot/artifact owner reference | Composite FK or centralized guard rejects. |
| EX04 | Two executable attempts inserted for one job | Partial unique index rejects the second. |
| EX05 | Submission fault after each insert | Job/attempt/queue/operation acceptance all roll back together. |
| EX06 | Equal submission keys from two processes | One job accepted; equivalent response after current authorization. |
| EX07 | Conflicting bytes/schema under equal key | Original remains unchanged; safe conflict audit, no second job. |
| EX08 | All Job source/destination pairs and actors | Exactly J01–J19; missing/invalid actor/guard rejects, no terminal reopening. |
| EX09 | All Attempt pairs and paired Job candidates | Exactly A01–A08 plus all cross-state invariants. |
| EX10 | Concurrent claimers for one queue row | One owner/epoch/analysis permit; losing transaction produces no attempt duplication. |
| EX11 | Two executing analyses; third accepted | Third remains persistent, becomes eligible only when capacity is safely available. |
| EX12 | Multiple accounts, one backlog/delayed head/locked row | FIFO within each account; other eligible account progresses; successful dispatch order is durable. |
| EX13 | Concurrent submissions at global/account admission boundary | At most configured outstanding bounds; retry does not allocate another admission slot. |
| EX14 | Crash after claim before any external operation | Database-time recovery retires old attempt; no new claim without safe local-stop/capacity proof. |
| EX15 | Crash after a completed step | Accepted step and exact bytes/binding persist; new attempt may reuse only same approved dependencies. |
| EX16 | Lease renewal races expiry/recovery | At boundary expiry rejects renewal; only one permitted new owner; old epoch never matches. |
| EX17 | Lock wait crosses expiry | Fresh time sampled after waits rejects stale publication/renewal. |
| EX18 | Heartbeat committed but acknowledgement lost | Reconcile same operation, no duplicate lease extension; no new work during ownership uncertainty. |
| EX19 | Two missed heartbeats and in-flight task | Stop-new-work/cleanup; threshold does not itself free lease/permit. |
| EX20 | Stale valid success/error/checkpoint | All active mutations reject; newer/terminal records remain intact. |
| EX21 | Final publication races cancellation | One guarded ordering; cancelled job cannot acquire final result, successful job cannot reopen. |
| EX22 | Claim races pending cancellation | One atomic winner; stale pending cancellation does not mutate running state without revalidation. |
| EX23 | Dead worker during cancellation | Controller finalizes J17; late history is separate, no indefinite acknowledgement dependency. |
| EX24 | Two recovery controllers | At most one replacement pending attempt/ordinal; monotonic epoch on claim. |
| EX25 | Fourth attempt requested with max three | Reject without count reset or terminal reopening. |
| EX26 | Database deadlock, known rollback | At most three DB executions, fresh guards; same operation, no scientific attempt increment or external replay. |
| EX27 | Connection failure during COMMIT | Outcome indeterminate until durable operation query; neither accepted nor rejected audit invented. |
| EX28 | Database retry exhaustion/heartbeat deadline | Bounded return with safe contention/unknown distinction; no unbounded pool/lock wait. |
| EX29 | Provider dispatch intent uncertain | J09/J10; external/global/per-analysis reservations remain held. |
| EX30 | Operator replacement authorization with unresolved old call | Cannot bypass retained concurrency/spend bounds; authorization is not settlement. |
| EX31 | Local process termination but external call continues | Analysis/process-stop proof and provider settlement are separate; provider permit remains. |
| EX32 | Terminal cancelled/failed job receives late provider response | Store safe settlement/history only; no active acceptance or state reopen. |
| EX33 | Counter release replay/capacity lowering | Release exactly once; counters equal live reservations; reject lowering below usage. |
| EX34 | Snapshot/classification/config/policy mismatch | Pin/guard failure; no latest-version or model substitution. |
| EX35 | Permission suspension/revocation races publication | All writers share guard ordering; revoked context cannot publish under stale read. |
| EX36 | Source/artifact deletion intent races publication | Ineligible guard rejects acceptance; no staged artifact appears in accepted view. |
| EX37 | Forged validation/typed absence/unknown schema | Whole-record validator rejects; no status-only bypass. |
| EX38 | Unconfigured production adapters | Explicit unavailable; test implementations cannot be selected by production environment. |
| EX39 | Cross-owner read/replay/copy references | No existence/private-data disclosure; accepted artifact owner FK enforces relationship. |
| EX40 | Missing physical object after prior acceptance | Download/export unavailable with safe diagnostic; no substituted file or claim of successful export. |
| EX41 | Manifest/output/resource overflow and malformed keys | Reject before unbounded parsing; no silent truncation or SQL interpolation. |
| EX42 | Complete outage during rejection audit | Return explicit uncertainty; recovery records what is known, not a fake committed event. |
| EX43 | Migration role versus worker role | Worker denied DDL/TRUNCATE; migration not run during import/startup. |
| EX44 | Existing Flask/contract/local runtime suite | Existing behavior preserved; no new background thread, data migration, frontend or provider call path. |
| EX45 | SQL/dependency inspection | Core only, bound queries, explicit Read Committed, no ORM/Session/direct driver write path or production create_all. |
| EX46 | Restore fixture DB records and immutable test-artifact manifest | Controlled infrastructure references and ownership remain consistent; not a substitute for P05 real DB/object backup acceptance. |

EX01–EX46 are a new execution-infrastructure specification family, not 46 executed tests or independent scientific cases. The existing 150 overlapping scientific/contract specification rows remain unchanged. A future test report must map each EX row to concrete test IDs, environment/version evidence, result and limitations; a green aggregate suite is not enough if rows are skipped.

## 4. Security and operational review

Test secrets must be generated per run and removed from logs/artifacts. No external networking/provider credentials in task tests. Object storage is a temporary fixture adapter only; no public download URLs or production bucket. Separate migration/runtime privilege failures are mandatory tests. Operators see safe correlation metadata, not arbitrary case contents. Direct DBA compromise, cloud outage and real provider behavior require deployment-specific validation beyond this harness.

The test profile's local process supervisor uses spawn plus process-group termination/reaping. After known parent/child loss on the same host, confirmed exit permits analysis-reservation release. For remote/uncertain host loss, retain reservations and require attributable operator stop evidence; automatic hosted failover is not claimed. Any hosted orchestration/process-isolation product remains open for P02/P06.

## 5. Development configuration additions

Preserve owner defaults exactly: lease 30 s, heartbeat 5 s, timeout 2 s, missed threshold two, polling allowed 1–3 s (recommend default two), three total scientific attempts, base two seconds/max fifteen/full jitter. Shared limits remain two analyses, one request per analysis, two globally. New recommended database-only timeout/pool/retry/admission settings are listed in the concrete SQL review and require coding-scope review. No values are approved for pilot/production by these documents.

Test provisioning and execution are proposed work AFTER explicit coding authorization. Do not run the future Compose profile, migrations or installation commands during design review.
