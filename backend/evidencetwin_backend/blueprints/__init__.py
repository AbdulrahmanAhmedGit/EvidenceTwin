"""Explicit domain blueprint registration; no automatic service discovery."""
from .system import bp as system_bp
from .analyses import bp as analyses_bp
from .evidence import bp as evidence_bp
from .visualizations import bp as visualizations_bp
from .council import bp as council_bp
from .audit import bp as audit_bp
from .reports import bp as reports_bp
from .comparisons import bp as comparisons_bp
from .benchmarks import bp as benchmarks_bp
from .integrations import bp as integrations_bp
from .cases import bp as cases_bp

BLUEPRINTS = (
    system_bp,
    analyses_bp,
    evidence_bp,
    visualizations_bp,
    council_bp,
    audit_bp,
    reports_bp,
    comparisons_bp,
    benchmarks_bp,
    integrations_bp,
    cases_bp,
)
