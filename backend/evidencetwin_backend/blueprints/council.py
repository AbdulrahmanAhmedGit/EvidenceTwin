"""Council transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("council", __name__, url_prefix="/api")

@bp.get("/analyses/<analysis_id>/council", strict_slashes=False)
def get_analysis_council(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>/council: analysis_id path; no body -> SectionResponse (reviews/disagreements).

    TODO (OWNER):
    - Responsibility/module: services.council: map actual owner independent/cross-review/judge
      results, citations, execution isolation and unresolved disputes; never infer truth from
      agreement.
    - Input: analysis_id path; no body.
    - Output: SectionResponse (reviews/disagreements); otherwise a consistent API error.
    - Frontend consumer: research-api.ts readAnalysisSection; CouncilView.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get analysis council is not implemented yet.")

