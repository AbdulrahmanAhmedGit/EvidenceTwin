"""Reports transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("reports", __name__, url_prefix="/api")

@bp.get("/analyses/<analysis_id>/report", strict_slashes=False)
def get_analysis_report(analysis_id: str) -> Response:
    """GET /api/analyses/<analysis_id>/report: analysis_id path; no body -> SectionResponse (report/sections).

    TODO (OWNER):
    - Responsibility/module: services.reports: retrieve an authorized real report with evidence-
      linked plain text and genuine references; expose actual JSON permission.
    - Input: analysis_id path; no body.
    - Output: SectionResponse (report/sections); otherwise a consistent API error.
    - Frontend consumer: research-api.ts readAnalysisSection; ResearchReport.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get analysis report is not implemented yet.")

@bp.get("/reports", strict_slashes=False)
def list_reports() -> Response:
    """GET /api/reports: ReportListQuery -> ReportList.

    TODO (OWNER):
    - Responsibility/module: services.reports: authorize search/date/status/mode/sort and pagination
      over reports that actually exist; report per-record permissions.
    - Input: ReportListQuery.
    - Output: ReportList; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readReports; Reports library.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List reports is not implemented yet.")

@bp.get("/reports/<report_id>", strict_slashes=False)
def get_report(report_id: str) -> Response:
    """GET /api/reports/<report_id>: report_id path; no body -> SectionResponse (report/sections).

    TODO (OWNER):
    - Responsibility/module: services.reports: retrieve the authorized report resource and actual
      export permission; reconcile report ID to its analysis without leaking another record.
    - Input: report_id path; no body.
    - Output: SectionResponse (report/sections); otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readReport; report preview/export.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Get report is not implemented yet.")

@bp.delete("/reports/<report_id>", strict_slashes=False)
def delete_report(report_id: str) -> Response:
    """DELETE /api/reports/<report_id>: report_id path; no body -> ActionAcknowledgement or HTTP 204.

    TODO (OWNER):
    - Responsibility/module: services.reports: authorize and delete only the intended report using
      owner retention policy; do not assume associated analysis deletion.
    - Input: report_id path; no body.
    - Output: ActionAcknowledgement or HTTP 204; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts deleteReport; Reports confirmation.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Delete report is not implemented yet.")

