"""Cases transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("cases", __name__, url_prefix="/api")

@bp.get("/cases", strict_slashes=False)
def list_research_cases() -> Response:
    """GET /api/cases: No body; query contract not yet defined -> JsonObject (owner contract pending).

    TODO (OWNER):
    - Responsibility/module: services.cases: agree the catalogue DTO with the owner/frontend before
      implementing authorized real case retrieval; do not copy educational fixtures into fake live
      results.
    - Input: No body; query contract not yet defined.
    - Output: JsonObject (owner contract pending); otherwise a consistent API error.
    - Frontend consumer: Reserved: React currently uses content/cases.ts locally.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List research cases is not implemented yet.")

@bp.get("/cases/<case_id>", strict_slashes=False)
def get_research_case(case_id: str) -> Response:
    """GET /api/cases/<case_id>: case_id path; no body -> JsonObject (owner contract pending).

    TODO (OWNER):
    - Responsibility/module: services.cases: agree the case DTO before implementing authorized real
      source/data/provenance retrieval; retain sample labels and unavailable uncertainty when
      appropriate.
    - Input: case_id path; no body.
    - Output: JsonObject (owner contract pending); otherwise a consistent API error.
    - Frontend consumer: Reserved: React currently uses content/cases.ts locally.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get research case is not implemented yet.")

