"""Comparisons transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("comparisons", __name__, url_prefix="/api")

@bp.get("/comparisons", strict_slashes=False)
def compare_analyses() -> Response:
    """GET /api/comparisons: ComparisonQuery (analysisA/analysisB) -> ComparisonResponse.

    TODO (OWNER):
    - Responsibility/module: services.comparisons: authorize both records and use owner
      comparability rules to return supplied dimensions/reasons with matching requested IDs; do not
      invent a winner.
    - Input: ComparisonQuery (analysisA/analysisB).
    - Output: ComparisonResponse; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readComparison; Comparison.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Compare analyses is not implemented yet.")

