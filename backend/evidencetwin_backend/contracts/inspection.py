from typing import Annotated, Literal, NotRequired
from pydantic import AfterValidator, Field
from .common import Wire, Timestamp, SourceStatus, PublicLink, JsonObject, NonNegativeInt, NonNegativeNumber, PositiveInt
from .analyses import Finding

class SectionPermissions(Wire):
    dataDownload: NotRequired[bool]
    contractDownload: NotRequired[bool]
    assetDownload: NotRequired[bool]
    auditDownload: NotRequired[bool]
    reportJson: NotRequired[bool]
class Source(Wire):
    id: str
    title: str
    status: SourceStatus
    checked: str
    url: NotRequired[PublicLink]
    date: NotRequired[str]
    limitations: NotRequired[list[str]]
    identifiers: NotRequired[dict[str, str]]
class UploadedFile(Wire):
    id: str
    name: str
    size: NonNegativeNumber
    mediaType: str
    status: str
    url: NotRequired[PublicLink]
class Variable(Wire):
    name: str
    unit: NotRequired[str]
    description: NotRequired[str]
    missingCount: NotRequired[NonNegativeInt]
class DatasetRecord(Wire):
    columns: Annotated[list[str], Field(min_length=1)]
    rows: Annotated[list[list[str | int | float | bool | None]], Field(max_length=5000)]
    variables: NotRequired[list[Variable]]
    serverPaginated: NotRequired[bool]
    totalRows: NotRequired[NonNegativeInt]
    page: NotRequired[PositiveInt]
    pageSize: NotRequired[PositiveInt]
    notes: NotRequired[list[str]]
def _dataset(value: DatasetRecord) -> DatasetRecord:
    if any(len(row) != len(value["columns"]) for row in value["rows"]):
        raise ValueError("Dataset rows must match columns")
    if value.get("serverPaginated") and not {"totalRows", "page", "pageSize"} <= value.keys():
        raise ValueError("Server pagination requires totalRows, page and pageSize")
    return value
Dataset = Annotated[DatasetRecord, AfterValidator(_dataset)]
class Legend(Wire):
    label: str
    color: Annotated[str, Field(pattern=r"^#[0-9a-fA-F]{6}$")]
class Interpretation(Wire):
    representation: Literal["original", "neutral"]
    text: str
    kind: NotRequired[Literal["interpretation", "source_backed"]]
class Visualization(Wire):
    changes: list[str]
    provenance: str
    original: NotRequired[PublicLink]
    neutral: NotRequired[PublicLink]
    compatible: NotRequired[bool]
    unavailableReason: NotRequired[str]
    originalDescription: NotRequired[str]
    neutralDescription: NotRequired[str]
    version: NotRequired[str]
    generationStatus: NotRequired[Literal["pending", "ready", "failed", "unavailable"]]
    warnings: NotRequired[list[str]]
    parameters: NotRequired[JsonObject]
    legend: NotRequired[list[Legend]]
    interpretations: NotRequired[list[Interpretation]]
    interpretationChanged: NotRequired[bool]
class Reviewer(Wire):
    id: str
    role: str
    phase: Literal["independent", "cross-review", "judge"]
    status: str
    summary: str
    findings: list[str]
    citations: list[str]
    roleKey: NotRequired[Literal["visual", "statistical", "scientific", "counterfactual"]]
    model: NotRequired[str]
    provider: NotRequired[str]
    independentExecution: NotRequired[bool]
    claims: NotRequired[list[str]]
    uncertainty: NotRequired[list[str]]
    report: NotRequired[JsonObject]
class Disagreement(Wire):
    claim: str
    positions: list[str]
    id: NotRequired[str]
    supportingEvidence: NotRequired[list[str]]
    contradictingEvidence: NotRequired[list[str]]
    status: NotRequired[Literal["resolved", "unresolved", "not_evaluated"]]
    resolution: NotRequired[str]
class AuditEvent(Wire):
    id: str
    timestamp: Timestamp
    component: str
    type: str
    status: str
    durationMs: NotRequired[NonNegativeNumber]
    inputRef: NotRequired[str]
    outputRef: NotRequired[str]
    error: NotRequired[str]
    metadata: NotRequired[JsonObject]
class ReportMetadata(Wire):
    title: NotRequired[str]
    generatedAt: NotRequired[Timestamp]
    version: NotRequired[str]
    reproducibility: NotRequired[str]
class Reference(Wire):
    title: str
    url: PublicLink
class ReportSection(Wire):
    id: str
    title: str
    body: str
    references: NotRequired[list[Reference]]
class SectionResponse(Wire):
    permissions: NotRequired[SectionPermissions]
    sources: NotRequired[list[Source]]
    files: NotRequired[list[UploadedFile]]
    dataset: NotRequired[Dataset]
    study: NotRequired[JsonObject]
    checks: NotRequired[list[Finding]]
    uncertainty: NotRequired[list[str]]
    contract: NotRequired[JsonObject]
    visualizations: NotRequired[Visualization]
    reviews: NotRequired[list[Reviewer]]
    disagreements: NotRequired[list[Disagreement]]
    events: NotRequired[list[AuditEvent]]
    report: NotRequired[ReportMetadata]
    sections: NotRequired[list[ReportSection]]
