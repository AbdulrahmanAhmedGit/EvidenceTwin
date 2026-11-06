"""Query-string shapes. Empty filters are valid and mean unrestricted."""
from datetime import date
from typing import Annotated, Literal, NotRequired, TypedDict
from pydantic import AfterValidator, Field
from .common import Wire, Status, Verdict, Mode, ResearchID, QueryInt

def _date_or_empty(value: str) -> str:
    if value:
        if len(value) != 10:
            raise ValueError("Expected YYYY-MM-DD")
        date.fromisoformat(value)
    return value
DateFilter = Annotated[str, AfterValidator(_date_or_empty)]
class ListQuery(Wire):
    search: NotRequired[str]
    page: NotRequired[Annotated[QueryInt, Field(ge=1)]]
    pageSize: NotRequired[Annotated[QueryInt, Field(ge=1, le=100)]]
class AnalysisListQuery(ListQuery):
    status: NotRequired[Status | Literal[""]]
    mode: NotRequired[Mode | Literal[""]]
    verdict: NotRequired[Verdict | Literal[""]]
    sort: NotRequired[Literal["createdAt:desc", "createdAt:asc", "title:asc", "status:asc", ""]]
class BenchmarkListQuery(ListQuery):
    status: NotRequired[Status | Literal[""]]
    sort: NotRequired[Literal["createdAt:desc", "createdAt:asc", "name:asc", ""]]
# Functional TypedDict construction retains reserved Python key `from` exactly.
ReportListQuery = TypedDict("ReportListQuery", {
    "search": NotRequired[str], "page": NotRequired[Annotated[QueryInt, Field(ge=1)]],
    "pageSize": NotRequired[Annotated[QueryInt, Field(ge=1, le=100)]],
    "status": NotRequired[Verdict | Literal[""]], "mode": NotRequired[Mode | Literal[""]],
    "from": NotRequired[DateFilter], "to": NotRequired[DateFilter],
    "sort": NotRequired[Literal["createdAt:desc", "createdAt:asc", "title:asc", ""]],
})
# Inherit the same strict behavior as other DTOs without changing wire keys.
ReportListQuery.__pydantic_config__ = Wire.__pydantic_config__
class DatasetQuery(Wire):
    page: Annotated[QueryInt, Field(ge=1)]
    pageSize: Annotated[QueryInt, Field(ge=25, le=25)]
    search: str
    sort: Annotated[QueryInt, Field(ge=-1)]
    direction: Literal["asc", "desc"]
class ComparisonQuery(Wire):
    analysisA: ResearchID
    analysisB: ResearchID
class ActivityQuery(Wire):
    limit: Annotated[QueryInt, Field(ge=1, le=100)]
