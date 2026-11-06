# EvidenceTwin Flask backend

Persistent local exploratory analyses, six server-side provider adapters, isolated
Council review, cross-review, model adjudication, audit and exploratory reports.
Scientific source/statistical verification, Neutral Twin generation, benchmark
scoring, authentication and MCP are explicitly unavailable until specified.

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
EVIDENCETWIN_CORS_ORIGINS=http://127.0.0.1:5202 .venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

Run from backend/. Set EVIDENCETWIN_PROVIDER, EVIDENCETWIN_MODEL and the selected
provider's server-side key to enable creation. No provider call occurs on startup.
No provider response is treated as independent scientific verification. Files and
records persist in instance/ by default. Use one process per workspace directory.

Read [BACKEND_IMPLEMENTATION_GUIDE.md](../BACKEND_IMPLEMENTATION_GUIDE.md) for all
routes, schemas, environment variables, architecture mapping, limits, cancellation,
source boundaries and remaining owner implementation responsibilities.


## Isolated PostgreSQL execution infrastructure

The existing Flask/local SQLite runtime is unchanged. The `execution/` package is an independently tested infrastructure path; HTTP submissions do not use it yet. No scientific task, real-provider call, source verification or authentication capability is enabled by this increment. All 24 design gates remain OPEN.

Install the tested environment with Python 3.14 (the repository backend venv is 3.14.4):

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip check
```

New tested pins are SQLAlchemy 2.1.8, Psycopg/psycopg-binary 3.3.8, Alembic 1.20.1 and Mako 1.4.3. Runtime persistence uses SQLAlchemy Core only. No ORM, Sessions, automatic schema creation or extra driver-level pool is used.

### Explicit disposable PostgreSQL tests

Tests require PostgreSQL 18.6 and its client utilities. They never use the application's `.env`, SQLite database or uploaded files. Without an explicit disposable test connection the required PostgreSQL suite fails rather than silently skipping. Ordinary legacy-only tests remain available with `python -m pytest tests --ignore=tests/execution`.

The verified route uses a private local Unix socket, no TCP listener and no system service changes. From the backend directory, when the PostgreSQL 18 binaries are installed:

```sh
cluster=$(mktemp -d /tmp/et_pg_XXXXXX)
chmod 700 "$cluster"
mkdir -m 700 "$cluster/socket"
/usr/lib/postgresql/18/bin/initdb -D "$cluster/data" -A trust --no-locale --encoding=UTF8
/usr/lib/postgresql/18/bin/pg_ctl -D "$cluster/data" -l "$cluster/server.log" -o "-k $cluster/socket -h '' -p 55439" -w start
export ET_EXECUTION_TEST_CLUSTER_DSN="postgresql+psycopg://$USER@/postgres?host=$cluster/socket&port=55439"
.venv/bin/python -m pytest tests -q
/usr/lib/postgresql/18/bin/pg_ctl -D "$cluster/data" -m fast -w stop
```

Remove only the recorded disposable `cluster` directory after confirming its server stopped; never run broad PostgreSQL-directory cleanup. Unix `trust` here is confined by the private mode-0700 parent/socket and disabled TCP. It is not a hosted authentication recommendation. Each test creates and removes a unique `et_test_<hex>` database and a DML-only runtime role. Fixture migrations use separate administrator access. No migrations run against application/production data.

An alternative opt-in `compose.execution-test.yaml` profile binds loopback on an ephemeral port and uses a per-run `ET_EXECUTION_TEST_PASSWORD`. It does not mount application files. Set `ET_EXECUTION_TEST_DISPOSABLE=1` and provide `ET_EXECUTION_TEST_CLUSTER_DSN` with `et_test_admin`, the mapped non-default loopback port and database `postgres`. The fixture also checks the container's `et_execution.test_cluster=enabled` sentinel. The Compose route was not executed in this environment; the native PostgreSQL route above was verified. No Docker installation/startup is performed by tests. Record a reviewed immutable image digest before adopting the Compose route in CI.

### Migration and worker boundaries

Alembic requires an explicit `ET_EXECUTION_TEST_ADMIN_DSN` targeting an already provisioned disposable `et_test_<hex>` database; it rejects other database names/destinations. Run `alembic -c alembic.ini upgrade head` only after deliberately selecting that isolated target. The pytest fixture does this automatically per test. Downgrade is destructive and is restricted by the same guard. Hosted migration support requires a later separately authorized scope.

`evidencetwin-worker --check` intentionally exits 2 with an unavailable message: no production task/auth/validation adapters are configured. It claims no jobs. Trusted application code can instantiate `Repository` and `Worker` with explicit reviewed adapters; test-only implementations live under `tests/execution`, not production. `Worker.run(stop_event)` polls using the configured interval. A supervisor and its stop-proof verifier must be the same configured instance. No arbitrary task-import command or automatic provider fallback exists.

Development defaults: lease 30 s; heartbeat 5 s; heartbeat deadline 2 s; missed threshold two; poll 2 s; three total execution attempts; retry base 2 s/cap 15 s/full jitter; two analyses, one LLM request per analysis and two globally. Database retries are separate: three total transactions for known deadlock/serialization aborts, 50/100 ms jitter bounds, with a two-second command deadline; heartbeat has one transaction per operation. Actual network/OS failure may leave a commit indeterminate: never claim a strict remote completion guarantee from timeouts alone.

Completed workflow output is not a verified scientific conclusion. Uncertain calls retain request permits. Terminal jobs may retain reservations until stop/settlement proof; lease expiry is never sufficient. See the implementation guide for results, recovery API and remaining integration gaps.
