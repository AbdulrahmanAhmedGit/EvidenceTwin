"""Integrations transport routes. Owner services are intentionally unimplemented."""
from flask import Blueprint, Response
from ..errors import not_implemented

bp = Blueprint("integrations", __name__, url_prefix="/api")

@bp.get("/integrations", strict_slashes=False)
def list_integrations() -> Response:
    """GET /api/integrations: No body -> IntegrationList.

    TODO (OWNER):
    - Responsibility/module: services.integrations: return only public, configured/planned
      availability metadata and real requirements/tool names; never expose keys, signed tokens or
      invented installation packages.
    - Input: No body.
    - Output: IntegrationList; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts readIntegrations; workspace management.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("List integrations is not implemented yet.")

@bp.post("/integrations/<integration_id>/test", strict_slashes=False)
def test_integration(integration_id: str) -> Response:
    """POST /api/integrations/<integration_id>/test: integration_id path; no body -> IntegrationTestResponse.

    TODO (OWNER):
    - Responsibility/module: services.integrations: authorize a configured connection test and
      report real reachable/failed status and check timestamp; this is not scientific validation or
      an MCP server implementation.
    - Input: integration_id path; no body.
    - Output: IntegrationTestResponse; otherwise a consistent API error.
    - Frontend consumer: features/research/api.ts testIntegration; integration test action.
    - Contract: docs/FRONTEND_API_CONTRACT.md; contracts/ and
      BACKEND_IMPLEMENTATION_GUIDE.md describe the exact wire fields.
    Do not substitute fixture results for this owner implementation.
    """
    return not_implemented("Test integration is not implemented yet.")

