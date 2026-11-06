"""Analyses transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("analyses", __name__, url_prefix="/api")

@bp.post("/analyses", strict_slashes=False)
def create_analysis() -> Response:
    """POST /api/analyses: multipart metadata: AnalysisCreateMetadata; repeated files parts -> AcceptedID.

    TODO (OWNER):
    - Responsibility/module: services.analyses: validate supplied metadata/files; authorize storage
      and invoke owner verification workflow; return ID only after actual acceptance.
    - Input: multipart metadata: AnalysisCreateMetadata; repeated files parts.
    - Output: AcceptedID; otherwise a consistent API error.
    - Frontend consumer: api.ts createAnalysis; AnalysisBuilder.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Create analysis is not implemented yet.")

@bp.get("/analyses", strict_slashes=False)
def list_analyses() -> Response:
    """GET /api/analyses: AnalysisListQuery -> AnalysisList.

    TODO (OWNER):
    - Responsibility/module: services.analyses: authorized search/filter/sort and server pagination
      over real records.
    - Input: AnalysisListQuery.
    - Output: AnalysisList; otherwise a consistent API error.
    - Frontend consumer: workspace-api.ts getAnalyses; dashboard/history/compare selectors.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List analyses is not implemented yet.")

@bp.get("/analyses/<analysis_id>", strict_slashes=False)
def get_analysis(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>: analysis_id path; no body -> Analysis.

    TODO (OWNER):
    - Responsibility/module: services.analyses: retrieve authorized record and actual job state;
      return exactly the requested ID and no synthesized stages.
    - Input: analysis_id path; no body.
    - Output: Analysis; otherwise a consistent API error.
    - Frontend consumer: research-api.ts readAnalysis; processing polling.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get analysis is not implemented yet.")

@bp.delete("/analyses/<analysis_id>", strict_slashes=False)
def delete_analysis(analysis_id: str) -> Response:
    """DELETE /api/analyses/<analysis_id>: analysis_id path; no body -> ActionAcknowledgement or HTTP 204.

    TODO (OWNER):
    - Responsibility/module: services.analyses: authorize deletion and owner-defined retention
      semantics; acknowledge only confirmed deletion.
    - Input: analysis_id path; no body.
    - Output: ActionAcknowledgement or HTTP 204; otherwise a consistent API error.
    - Frontend consumer: workspace-api.ts deleteAnalysis; history confirmation.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Delete analysis is not implemented yet.")

@bp.post("/analyses/<analysis_id>/retry", strict_slashes=False)
def retry_analysis(analysis_id: str) -> Response:
    """POST /api/analyses/<analysis_id>/retry: analysis_id path; no body -> ActionAcknowledgement.

    TODO (OWNER):
    - Responsibility/module: services.analyses: authorize retry, verify state/eligibility and
      request real owner job restart; return confirmed acknowledgement.
    - Input: analysis_id path; no body.
    - Output: ActionAcknowledgement; otherwise a consistent API error.
    - Frontend consumer: workspace-api.ts retryAnalysis; research-api.ts analysisAction.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Retry analysis is not implemented yet.")

@bp.post("/analyses/<analysis_id>/cancel", strict_slashes=False)
def cancel_analysis(analysis_id: str) -> Response:
    """POST /api/analyses/<analysis_id>/cancel: analysis_id path; no body -> ActionAcknowledgement.

    TODO (OWNER):
    - Responsibility/module: services.analyses: authorize cancellation and connect actual job
      transport; acknowledge request, expose resulting state via record reads.
    - Input: analysis_id path; no body.
    - Output: ActionAcknowledgement; otherwise a consistent API error.
    - Frontend consumer: research-api.ts analysisAction; confirmation dialog.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Cancel analysis is not implemented yet.")

