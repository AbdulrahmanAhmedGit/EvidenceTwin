# EvidenceTwin V1 — Dependency compatibility review

**Status: Recommended for owner approval.** Researched 2026-11-06. All **24 gates remain OPEN**. No package was installed, downloaded as an executable wheel, upgraded or added to a project dependency file. Research queried official PyPI JSON metadata and primary project documentation; the checks below are static metadata checks, not a resolver/ABI/runtime compatibility certification.

## Proposed first implementation environment

Recommend the existing backend Python **3.14.4** environment, conventional GIL-enabled CPython on Linux x86_64. The generic shell inspection interpreter is Python 3.15.0; do not accidentally resolve/install against it. The project virtual environment and /usr/bin/python3 report 3.14.4. Preserve Python >=3.12 as the existing package compatibility declaration unless actual supported-version tests justify changing it; first-increment acceptance targets 3.14.4, not a claim that every supported Python was exercised.

Recommend PostgreSQL **18.6** for isolated development and hosted testing of this increment. The official supported-version table listed 18.6 as the current 18 minor when researched. Recheck patch/security notices before future installation; pin the actual tested image/package identity, not a mutable latest tag. No provider/region/hosted deployment is selected.

| Package | Proposed research pin | Requires-Python | Distribution evidence |
| --- | --- | --- | --- |
| Flask | 3.1.3 | >=3.9 | Universal Python wheel observed |
| SQLAlchemy | 2.1.8 | >=3.11 | CPython 3.14 Linux x86_64 wheel observed |
| psycopg | 3.3.8 | >=3.10 | Universal Python wheel observed |
| psycopg-binary | 3.3.8 | >=3.10 | CPython 3.14 Linux x86_64 wheel observed |
| alembic | 1.20.1 | >=3.10 | Universal Python wheel observed |
| Mako | 1.4.3 | >=3.10 | Universal Python wheel observed |
| typing-extensions | 4.16.0 | >=3.9 | Universal Python wheel observed |
| pytest | 9.2.0 | >=3.10 | Universal Python wheel observed |

Only SQLAlchemy **2.1.8**, psycopg[binary] **3.3.8**, Alembic **1.20.1** and Alembic's Mako **1.4.3** are new implementation dependencies proposed here. Existing Flask **3.1.3**, pytest **9.2.0** and typing-extensions **4.16.0** already match the existing lock. Keep the other existing pins unchanged unless an authorized resolver demonstrates a necessary conflict. Do not introduce greenlet/asyncio extras, psycopg_pool, Flask-SQLAlchemy or an ORM integration. Synchronous Core does not require the asyncio extra.

Recommended declared version families after authorization: SQLAlchemy >=2.1.8,<2.2; psycopg[binary] >=3.3.8,<3.4; Alembic >=1.20.1,<1.21. Resolve and lock exact tested versions plus all transitives; recommendation is not permission to edit pyproject/lock now. Binary Psycopg is recommended for the initial reproducible Linux test environment to avoid an unplanned compiler/libpq build. Its bundled native libraries require regular patch/security review; a future hosted image may choose a system-linked build only through explicit reviewed deployment configuration.

## Checks actually performed

1. Read existing backend pyproject, requirements.lock, factory, config, local Store/Workflow and test fixtures without importing the application or reading instance data/secrets.
2. Retrieved current official PyPI metadata for the packages above. Static specifier checks accepted Python 3.14.4 for all researched packages.
3. Verified Alembic's declared SQLAlchemy >=2.0 accepts proposed 2.1.8; SQLAlchemy's Psycopg driver requirement accepts 3.3.8; psycopg[binary] selects the matching psycopg-binary 3.3.8.
4. Observed universal wheels for Python-only packages and matching cp314 standard-ABI manylinux x86_64 wheels for SQLAlchemy and psycopg-binary. This does not test libc, architecture, native import or a free-threaded Python build.
5. Reviewed SQLAlchemy's PostgreSQL Psycopg dialect, Core transaction APIs and Alembic migration environment. Flask has no SQLAlchemy integration dependency here: it remains the existing HTTP framework, while the worker is independently executable.

Mako requires MarkupSafe >=2.0; the existing 3.0.4 pin satisfies it. Static marker/specifier review checked 15 active direct dependency edges across Flask, SQLAlchemy, Psycopg, Alembic, Mako and pytest against the proposed/existing pins and identified no conflict or missing pin among those edges. The complete closure still requires the authorized full resolver; these checks are not a resolver run. A full pip resolution/install/import/database test has NOT been run; do not report dependencies as runtime-validated.

## Authorized implementation checks required later

Use the backend 3.14 environment (or an isolated matching test venv); resolve the entire existing+new package set, inspect the proposed lock delta, reject prereleases unless separately justified, then perform installation/import smoke tests and pip check. Verify `postgresql+psycopg` selects Psycopg 3, Engine isolation is READ COMMITTED, parameter binding works, server reports expected major/minor, Alembic runs only explicitly, and existing Flask/local-runtime tests still pass. Do not execute live provider requests during smoke tests.

If compatible wheels, registry access or the approved test server are unavailable, report an implementation blocker rather than silently switching driver, Python, PostgreSQL or dependency family. Major/minor recommendations remain unapproved recommendations until the coding scope is authorized; no gate is closed by this research.

## Sources

- [Flask 3.1.3 metadata](https://pypi.org/pypi/Flask/3.1.3/json).
- [SQLAlchemy 2.1.8 metadata](https://pypi.org/pypi/SQLAlchemy/2.1.8/json), [Core 2.1 documentation](https://docs.sqlalchemy.org/en/21/core/connections.html), [Psycopg dialect](https://docs.sqlalchemy.org/en/21/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg).
- [Psycopg 3.3.8 metadata](https://pypi.org/pypi/psycopg/3.3.8/json), [binary wheel metadata](https://pypi.org/pypi/psycopg-binary/3.3.8/json), [installation variants](https://www.psycopg.org/psycopg3/docs/basic/install.html). The moving Psycopg documentation identifies a development build; that is not the selected install version.
- [Alembic 1.20.1 metadata](https://pypi.org/pypi/alembic/1.20.1/json), [migration tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [Mako 1.4.3 metadata](https://pypi.org/pypi/Mako/1.4.3/json).
- [PostgreSQL supported versions](https://www.postgresql.org/support/versioning/).
