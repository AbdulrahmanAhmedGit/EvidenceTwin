from typing import Annotated, Literal, NotRequired
from datetime import date
from pydantic import AfterValidator, Field
from .common import JsonObject, Wire, Page, Status, Verdict, Mode, SourceStatus, Timestamp, NonNegativeNumber, ResearchID

def _nonblank(value: str) -> str:
    if not value.strip():
        raise ValueError("Claim cannot be blank")
    return value
Claim = Annotated[str, Field(min_length=1, max_length=10000), AfterValidator(_nonblank)]
def _study_date(value: str) -> str:
    if value:
        if len(value) != 10:
            raise ValueError("Expected YYYY-MM-DD")
        date.fromisoformat(value)
    return value

class AnalysisCreateMetadata(Wire):
    """The JSON `metadata` multipart field; files are separate repeated parts."""
    source: Annotated[str, Field(max_length=500)]
    url: Annotated[str, Field(max_length=2000)]
    studyDate: Annotated[str, Field(max_length=10), AfterValidator(_study_date)]
    studyDesign: Literal["Unknown", "Randomized experimental", "Observational", "Cross-sectional", "Repeated cross-sectional", "Longitudinal", "Meta-analysis", "Other"]
    population: Annotated[str, Field(max_length=3000)]
    uncertainty: Annotated[str, Field(max_length=3000)]
    context: Annotated[str, Field(max_length=5000)]
    claims: Annotated[list[Claim], Field(min_length=1, max_length=10)]
    claim: Claim
    mode: Mode
    reviewDepth: Literal["focused", "council"]
    caseId: NotRequired[Literal["a1", "a2", "a3"]]

class AcceptedID(Wire):
    id: ResearchID
# No acknowledgement fields are currently consumed by React.
ActionAcknowledgement = JsonObject

class Finding(Wire):
    kind: Literal["calculation", "source_backed", "interpretation", "unverified"]
    text: str
    citations: list[str]
    id: NotRequired[str]
    value: NotRequired[str | int | float]
    unit: NotRequired[str]
    sourceVerified: NotRequired[bool]
class Actions(Wire):
    retry: NotRequired[bool]
    cancel: NotRequired[bool]
class Stage(Wire):
    id: str
    label: str
    status: Literal["pending", "running", "completed", "failed", "skipped"]
    timestamp: NotRequired[Timestamp]
    durationMs: NotRequired[NonNegativeNumber]
class ReviewSummary(Wire):
    role: str
    status: str
    summary: str
class Analysis(Wire):
    id: str
    title: str
    status: Status
    mode: Mode
    createdAt: Timestamp
    claim: str
    limitations: list[str]
    findings: list[Finding]
    startedAt: NotRequired[Timestamp]
    claims: NotRequired[list[str]]
    stage: NotRequired[str]
    stages: NotRequired[list[Stage]]
    assessment: NotRequired[Verdict]
    sourceStatus: NotRequired[SourceStatus]
    issues: NotRequired[list[str]]
    suggestedInterpretation: NotRequired[str]
    error: NotRequired[str]
    actions: NotRequired[Actions]
    reviewSummary: NotRequired[list[ReviewSummary]]
class AnalysisRecord(Wire):
    id: str
    title: str
    createdAt: Timestamp
    status: Status
    mode: Mode
    source: NotRequired[str]
    assessment: NotRequired[Verdict]
    summary: NotRequired[str]
    reportAvailable: NotRequired[bool]
class AnalysisList(Page):
    items: list[AnalysisRecord]
