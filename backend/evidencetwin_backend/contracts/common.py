"""Wire DTOs only: camelCase matches React; validation is not verification."""
from datetime import datetime
import re
from typing import Annotated, Literal, TypedDict, TypeVar, Any
from urllib.parse import urlsplit, parse_qsl

from pydantic import AfterValidator, BeforeValidator, ConfigDict, Field, JsonValue, TypeAdapter, with_config

@with_config(ConfigDict(strict=True, extra="forbid", allow_inf_nan=False))
class Wire(TypedDict):
    """NotRequired means absent is allowed; it does not mean null is allowed."""

T = TypeVar("T")
def validate_contract(schema: Any, payload: T) -> T:
    """Validate a DTO without calculating, fetching, persisting or adjudicating."""
    return TypeAdapter(schema).validate_python(payload, strict=True)

NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveInt = Annotated[int, Field(ge=1)]
NonNegativeNumber = Annotated[float, Field(ge=0, allow_inf_nan=False)]
ResearchID = Annotated[str, Field(min_length=1, max_length=200)]
Status = Literal["draft", "awaiting_evidence", "queued", "running", "completed", "completed_with_limitations", "failed", "cancelled"]
Verdict = Literal["supported", "unsupported", "partially_supported", "insufficient_evidence", "unresolved", "not_evaluated"]
Mode = Literal["verified", "exploratory"]
SourceStatus = Literal["verified", "partially_verified", "unverified", "unavailable", "unknown"]
JsonObject = dict[str, JsonValue]

def _timestamp(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})", value):
        raise ValueError("Expected an ISO timestamp with timezone")
    datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value
Timestamp = Annotated[str, AfterValidator(_timestamp)]

def _link(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.username or parsed.password:
        raise ValueError("URLs must not contain credentials")
    absolute = parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)
    relative = value.startswith("/") and not value.startswith("//") and not parsed.netloc
    if not (absolute or relative):
        raise ValueError("Expected HTTP(S) or a same-origin path")
    return value
PublicLink = Annotated[str, AfterValidator(_link)]

def _integration_link(value: str) -> str:
    _link(value)
    if any(re.search(r"token|secret|key|password|credential", key, re.I) for key, _ in parse_qsl(urlsplit(value).query)):
        raise ValueError("Public integration URLs cannot carry credentials")
    return value
IntegrationLink = Annotated[str, AfterValidator(_integration_link)]

def _query_integer(value: object) -> object:
    if isinstance(value, str):
        if not re.fullmatch(r"-?\d+", value):
            raise ValueError("Expected an integer query string")
        return int(value)
    return value
QueryInt = Annotated[int, BeforeValidator(_query_integer)]

class Page(Wire):
    total: NonNegativeInt
    page: PositiveInt
    pageSize: PositiveInt

class ResearchPage(Wire):
    total: NonNegativeInt
    page: PositiveInt
    pageSize: Annotated[int, Field(ge=1, le=100)]
