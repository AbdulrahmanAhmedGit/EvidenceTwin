# Application services

`runtime.py` binds legacy HTTP services, ingestion, authorized retrieval and truthful capabilities. `store.py` persists private SQLite JSON records and files. `research_cases.py` adds immutable revisions and explicit run acceptance; `access.py` provides optional invite-only sessions, ownership and operator enforcement. `workflow.py` runs local threaded exploratory jobs and preserves audit/report history. `provider.py`, `transports.py` and `ai_settings.py` configure server-side model execution and schema/reference validation.

See [architecture](../../../docs/ARCHITECTURE.md) and [API](../../../docs/API.md). The independent `execution/` PostgreSQL package is not the HTTP runtime. Model review is not scientific verification.
