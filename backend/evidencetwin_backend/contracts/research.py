from typing import Annotated, Literal, NotRequired
from pydantic import AfterValidator, BeforeValidator, Field, StringConstraints
from .common import Wire, ResearchPage, ResearchID, Timestamp, Status, Verdict, Mode, NonNegativeInt, PositiveInt, NonNegativeNumber, IntegrationLink

class ComparisonDimension(Wire):
    key: ResearchID
    label: str
    a: str | None
    b: str | None
    relation: Literal["same", "different", "not_comparable", "unknown"]
    note: NotRequired[str]
class ComparisonResponse(Wire):
    analysisA: ResearchID
    analysisB: ResearchID
    comparability: Literal["comparable", "limited", "incompatible", "unknown"]
    reasons: list[str]
    dimensions: list[ComparisonDimension]
Condition = Literal["standard", "evidence_first", "deterministic", "council"]
def _unique_ids(ids: list[str]) -> list[str]:
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate case references")
    return ids
def _true(value: object) -> object:
    if value is not True:
        raise ValueError("preserveControls must be true")
    return value
class BenchmarkCreate(Wire):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=160)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=4000)]
    caseIds: Annotated[list[ResearchID], Field(min_length=1), AfterValidator(_unique_ids)]
    conditions: Annotated[list[Condition], Field(min_length=2)]
    modelConfigRef: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    rubricRef: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    repetitions: Annotated[int, Field(ge=1, le=100)]
    seed: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    preserveControls: Annotated[Literal[True], BeforeValidator(_true)]
    outputs: Annotated[list[Literal["summary", "per_case", "audit"]], Field(min_length=1)]
class BenchmarkSummary(Wire):
    id: ResearchID
    name: str
    description: str
    createdAt: Timestamp
    status: Status
    caseCount: NonNegativeInt
    conditions: list[str]
    availableMetrics: NotRequired[list[str]]
    completedRuns: NotRequired[NonNegativeInt]
    totalRuns: NotRequired[PositiveInt]
class MetricRecord(Wire):
    key: ResearchID
    label: str
    definition: str
    value: NonNegativeNumber | None
    unit: Literal["rate", "count", "milliseconds", "currency"]
    condition: str
    numerator: NotRequired[NonNegativeInt]
    denominator: NotRequired[PositiveInt]
    currency: NotRequired[str]
    limitations: NotRequired[list[str]]
def _metric(value: MetricRecord) -> MetricRecord:
    # Frontend wire constraints only. Do not calculate a metric or infer a rate.
    if value["unit"] == "rate" and value["value"] is not None:
        if value["value"] > 1 or "denominator" not in value:
            raise ValueError("Measured rates require a denominator and value within [0, 1]")
    if "numerator" in value and "denominator" in value and value["numerator"] > value["denominator"]:
        raise ValueError("Numerator exceeds denominator")
    if value["unit"] == "currency" and value["value"] is not None and not value.get("currency"):
        raise ValueError("Measured cost requires currency")
    return value
Metric = Annotated[MetricRecord, AfterValidator(_metric)]
class BenchmarkCase(Wire):
    caseId: ResearchID
    title: str
    condition: str
    status: str
    outcome: str | None
    analysisId: NotRequired[ResearchID]
    failure: NotRequired[str]
class BenchmarkPermissions(Wire):
    json: NotRequired[bool]
class BenchmarkResponse(BenchmarkSummary):
    configuration: BenchmarkCreate
    metrics: list[Metric]
    limitations: list[str]
    cases: list[BenchmarkCase]
    reproducibility: NotRequired[str]
    permissions: NotRequired[BenchmarkPermissions]
class BenchmarkList(ResearchPage):
    items: list[BenchmarkSummary]
class ReportPermissions(Wire):
    delete: NotRequired[bool]
    json: NotRequired[bool]
class ReportRecord(Wire):
    id: ResearchID
    analysisId: ResearchID
    title: str
    createdAt: Timestamp
    status: Verdict
    mode: Mode
    summary: NotRequired[str]
    permissions: NotRequired[ReportPermissions]
class ReportList(ResearchPage):
    items: list[ReportRecord]
class Integration(Wire):
    id: ResearchID
    name: str
    category: Literal["mcp", "skill", "api", "developer"]
    status: Literal["available", "configured", "not_configured", "planned", "unsupported"]
    overview: str
    capabilities: list[str]
    requirements: list[str]
    instructions: list[str]
    documentation: Literal["api", "mcp", "skills", "getting-started"]
    endpoint: NotRequired[IntegrationLink]
    authentication: NotRequired[str]
    tools: NotRequired[list[str]]
    trigger: NotRequired[str]
    canTest: NotRequired[bool]
class IntegrationList(Wire):
    items: list[Integration]
class IntegrationTestResponse(Wire):
    status: Literal["reachable", "failed"]
    message: str
    checkedAt: Timestamp
