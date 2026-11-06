"""Reachability and truthful, public, non-secret capability metadata."""
from flask import Blueprint, Response, jsonify, current_app
from ..contracts.common import validate_contract
from ..contracts.system import CapabilitiesResponse, HealthResponse
from .. import API_VERSION
from ..errors import not_implemented

bp = Blueprint("system", __name__, url_prefix="/api")

@bp.get("/health", strict_slashes=False)
def health() -> Response:
    """No input -> HealthResponse; api.ts health()/ConnectionBadge.

    This only establishes that Flask can answer. No scientific dependency is probed.
    See docs/FRONTEND_API_CONTRACT.md, Implemented frontend calls.
    """
    payload: HealthResponse = {"status": "ok", "apiVersion": API_VERSION,
                               "mode": "workspace" if current_app.config["RUNTIME_ENABLED"] else "integration_skeleton", "scientificServices": "unavailable"}
    return jsonify(validate_contract(HealthResponse, payload))

@bp.get("/capabilities", strict_slashes=False)
def capabilities() -> Response:
    """No input -> CapabilitiesResponse; workspace and research capability hooks.

    TODO (OWNER): after implementing/authorizing each actual service, map its
    availability here. Enable only capabilities backed by tested routes/services;
    never turn a flag on merely because a stub is registered. Input is trusted
    server service configuration, output remains the frontend capability contract.
    See docs/FRONTEND_API_CONTRACT.md, Phase 3/5 capability contracts.
    """
    payload: CapabilitiesResponse = {
        "providers": [], "jobAvailability": "unavailable", "activity": False,
        "analyses": {"create": False, "delete": False, "retry": False,
                     "maxClaims": 1, "modes": [], "reviewDepths": []},
        "services": [{"name": name, "status": "unavailable"} for name in (
            "Scientific Core", "Source verification", "Neutral visualization",
            "Council", "Evidence Judge", "Reports", "Benchmarks", "MCP")],
        "research": {"comparison": False, "benchmarks": {"read": False, "create": False},
                     "reports": {"read": False}, "integrations": {"read": False}},
    }
    return jsonify(validate_contract(CapabilitiesResponse, payload))

@bp.get("/activity", strict_slashes=False)
def list_activity() -> Response:
    """ActivityQuery -> ActivityResponse; WorkspaceHome.getActivity().

    TODO (OWNER):
    - Responsibility/module: services.activity reads authorized real audit/activity records.
    - Input: ActivityQuery with the requested limit.
    - Output: ActivityResponse with actual timestamps and optional analysis IDs.
    - Frontend consumer: workspace-api.ts getActivity / WorkspaceHome recent activity.
    Enable capabilities.activity only after retrieval and authorization work.
    See docs/FRONTEND_API_CONTRACT.md, Phase 3 creation and settings update.
    """
    return not_implemented("Workspace activity retrieval is not implemented yet.")
