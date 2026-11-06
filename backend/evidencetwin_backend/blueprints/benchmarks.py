"""Benchmarks transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("benchmarks", __name__, url_prefix="/api")

@bp.post("/benchmarks", strict_slashes=False)
def create_benchmark() -> Response:
    """POST /api/benchmarks: JSON BenchmarkCreate -> AcceptedID.

    TODO (OWNER):
    - Responsibility/module: services.benchmarks: authorize and validate
      configuration/cases/model/rubric references; enforce owner control protocol and accept a real
      evaluation run; return its ID.
    - Input: JSON BenchmarkCreate.
    - Output: AcceptedID; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts createBenchmark; BenchmarkBuilder.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Create benchmark is not implemented yet.")

@bp.get("/benchmarks", strict_slashes=False)
def list_benchmarks() -> Response:
    """GET /api/benchmarks: BenchmarkListQuery -> BenchmarkList.

    TODO (OWNER):
    - Responsibility/module: services.benchmarks: authorized paginated search/filter/sort over
      actual run metadata; do not produce synthetic metrics or progress.
    - Input: BenchmarkListQuery.
    - Output: BenchmarkList; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readBenchmarks; BenchmarkList.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List benchmarks is not implemented yet.")

@bp.get("/benchmarks/<benchmark_id>", strict_slashes=False)
def get_benchmark(benchmark_id: str) -> Response:
    """GET /api/benchmarks/<benchmark_id>: benchmark_id path; no body -> BenchmarkResponse.

    TODO (OWNER):
    - Responsibility/module: services.benchmarks: return the matching real run, configuration,
      actual measurements/denominators/failures and limitations; preserve unavailable metrics as
      null.
    - Input: benchmark_id path; no body.
    - Output: BenchmarkResponse; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readBenchmark; BenchmarkDetail polling.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get benchmark is not implemented yet.")

