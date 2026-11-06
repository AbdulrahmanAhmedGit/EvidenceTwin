"""Named request/response schemas for owner tooling and handoff checks."""
from .ai import AISettingsInput, AISettingsPublic
from .analyses import AnalysisCreateMetadata, AcceptedID, ActionAcknowledgement, Analysis, AnalysisList
from .common import JsonObject
from .inspection import SectionResponse, Dataset
from .research import BenchmarkCreate, BenchmarkResponse, BenchmarkList, ReportList, IntegrationList, IntegrationTestResponse, ComparisonResponse
from .queries import ActivityQuery, AnalysisListQuery, BenchmarkListQuery, ReportListQuery, DatasetQuery, ComparisonQuery
from .system import HealthResponse, CapabilitiesResponse, ActivityResponse
from ..errors import ErrorResponse

SCHEMAS = {name: value for name, value in globals().copy().items()
           if name not in {"SCHEMAS"} and not name.startswith("_")}
