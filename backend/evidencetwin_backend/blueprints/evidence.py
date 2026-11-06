"""Evidence transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("evidence", __name__, url_prefix="/api")

@bp.get("/analyses/<analysis_id>/evidence", strict_slashes=False)
def get_analysis_evidence(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>/evidence: analysis_id path; no body -> SectionResponse (evidence fields).

    TODO (OWNER):
    - Responsibility/module: services.evidence: authorize access and map supplied/verified source,
      file, dataset and evidence-contract records; distinguish computed facts from source
      authentication.
    - Input: analysis_id path; no body.
    - Output: SectionResponse (evidence fields); otherwise a consistent API error.
    - Frontend consumer: research-api.ts readAnalysisSection; EvidenceInspector.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get analysis evidence is not implemented yet.")

@bp.get("/analyses/<analysis_id>/dataset", strict_slashes=False)
def get_analysis_dataset(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>/dataset: analysis_id path; DatasetQuery -> Dataset.

    TODO (OWNER):
    - Responsibility/module: services.evidence: apply authorized full-dataset search/sort and return
      the requested 25-row page with matching columns/page metadata; do not impute data.
    - Input: analysis_id path; DatasetQuery.
    - Output: Dataset; otherwise a consistent API error.
    - Frontend consumer: research-api.ts readDataset; DatasetViewer.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get analysis dataset is not implemented yet.")

