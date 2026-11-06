"""Audit transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("audit", __name__, url_prefix="/api")

@bp.get("/analyses/<analysis_id>/audit", strict_slashes=False)
def list_analysis_audit(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>/audit: analysis_id path; no body -> SectionResponse (events).

    TODO (OWNER):
    - Responsibility/module: services.audit: authorize real chronological events with actual
      timestamps/references; sanitize secrets before any serialization or download.
    - Input: analysis_id path; no body.
    - Output: SectionResponse (events); otherwise a consistent API error.
    - Frontend consumer: research-api.ts readAnalysisSection; AuditTrail.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List analysis audit is not implemented yet.")

