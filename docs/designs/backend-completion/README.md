# Backend design and scientific decision index

These documents preserve proposals, scoped decisions and review history. Read the [documentation authority](../../DOCUMENTATION_MAP.md) and [current scientific scope](../../SCIENTIFIC_SCOPE.md) before implementing a procedure. All 24 gates remain OPEN. The [approved root brief](../../../concepts_brief.md) has precedence over the nested frozen review brief.

The root [design draft](../../../design_draft.md) records scoped approvals. Later bounded infrastructure selections do not authorize unspecified scientific methods or hosted execution. Current application behavior is described in [Architecture](../../ARCHITECTURE.md) and [API](../../API.md).

## Approval boundaries and reading order

- [EvidenceTwin V1 — Technical Plan gate register](TECHNICAL_PLAN_GATES.md)
- [EvidenceTwin V1 — Consolidated open decisions](OPEN_DECISIONS.md)
- [EvidenceTwin V1 — Proposed Q01–Q60 policy package](RECOMMENDED_DECISIONS.md)
- [EvidenceTwin V1 — Coding Readiness Report](CODING_READINESS_REPORT.md)
- [EvidenceTwin V1 — First coding scope and readiness decisions](FIRST_CODING_SCOPE.md)
- [EvidenceTwin V1 — First implementation file and test mapping](FIRST_IMPLEMENTATION_FILE_MAP.md)
- [EvidenceTwin V1 — Scientific applicability and verification specification](SCIENTIFIC_SPECIFICATION_DRAFT.md)

## Scientific procedures and review contracts

- [EvidenceTwin V1 — R01–R07 scientific contract refinement](SCIENTIFIC_CONTRACTS_DRAFT.md)
- [EvidenceTwin V1 — R04 source retrieval, proof and temporal contracts](SOURCE_PROCEDURES_DRAFT.md)
- [EvidenceTwin V1 — R02 numerical contracts and precision](NUMERICAL_CONTRACTS_DRAFT.md)
- [EvidenceTwin V1 — Decimal arithmetic and explicit conversion boundaries](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md)
- [EvidenceTwin V1 — R03 statistical request, prerequisite and result contracts](STATISTICAL_CONTRACTS_DRAFT.md)
- [EvidenceTwin V1 — R06 Council packets, phases and evidence judging](COUNCIL_REVIEW_CONTRACTS_DRAFT.md)
- [EvidenceTwin V1 — R05 researcher confirmation and revision contracts](CONFIRMATION_REVISION_CONTRACTS_DRAFT.md)
- [EvidenceTwin V1 — R07 versioned acceptance-corpus contract](ACCEPTANCE_CORPUS_CONTRACT_DRAFT.md)
- [EvidenceTwin V1 — R01–R07 cross-contract consistency review](CROSS_CONTRACT_REVIEW.md)

## Evidence, check and publication schemas

- [EvidenceTwin V1 — R01 canonical check representation options](CANONICAL_CHECK_CONTRACT_OPTIONS.md)
- [EvidenceTwin V1 — FD01–FD02 canonical schema and publication proposal](CANONICAL_SCHEMA_PUBLICATION_PROPOSAL.md)
- [EvidenceTwin V1 — Independent typed check dimensions](TYPED_CHECK_AXES_DRAFT.md)
- [EvidenceTwin V1 — Explicit typed absence and unresolved applicability](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md)
- [EvidenceTwin V1 — Check lifecycle and guarded publication](CHECK_LIFECYCLE_PUBLICATION_DRAFT.md)
- [EvidenceTwin V1 — Candidate publication guard schemas](PUBLICATION_GUARD_SCHEMA_PROPOSAL.md)
- [EvidenceTwin V1 — FD02 publication and idempotency options](PUBLICATION_IDEMPOTENCY_OPTIONS.md)
- [EvidenceTwin V1 — Conditional publication, monotonic fencing and guard coverage](VERSION_GUARDED_PUBLICATION_DRAFT.md)

## Execution, transactions and recovery

- [EvidenceTwin V1 — Core repository and transaction contract](CORE_TRANSACTION_PLAN_DRAFT.md)
- [EvidenceTwin V1 — Short-transaction consistency choice](TRANSACTION_CONSISTENCY_OPTIONS.md)
- [EvidenceTwin V1 — Separate Job and Execution Attempt transition tables](JOB_ATTEMPT_TRANSITIONS_DRAFT.md)
- [EvidenceTwin V1 — Lease, retry and reconciliation rules](LEASE_RETRY_RECONCILIATION_DRAFT.md)
- [EvidenceTwin V1 — Concrete execution schema and SQL review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md)
- [EvidenceTwin V1 — Execution metadata, constraints and statement map](EXECUTION_SCHEMA_STATEMENT_MAP.md)
- [EvidenceTwin V1 — Execution integration environment and acceptance specification](EXECUTION_TEST_SPECIFICATION.md)
- [EvidenceTwin V1 — PostgreSQL access and migration tooling choice](POSTGRESQL_TOOLING_OPTIONS.md)
- [EvidenceTwin V1 — Dependency compatibility review](DEPENDENCY_COMPATIBILITY_REVIEW.md)

## Frozen reviews and reference investigation

- [Goldfish review synthesis](2026-11-05-goldfish/goldfish_review_report.md), [review intake](2026-11-05-goldfish/review_input.md) and [frozen concepts brief](2026-11-05-goldfish/concepts_brief.md). The six raw lens reports remain alongside the synthesis.
- [Ember acceptance investigation](ember-2025-acceptance/acceptance_case.md). Its reference artifacts retain incomplete historical input identity and original-chart access boundaries. This is preserved research, without a claim of passed scientific execution.

Keep approval status, dates, unresolved questions and reproducibility records intact. Add an attributable decision when a choice changes, then update the current guide after implementation is verified.
