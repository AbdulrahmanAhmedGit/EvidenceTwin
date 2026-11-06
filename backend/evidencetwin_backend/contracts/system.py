from typing import Annotated, Literal, NotRequired
from pydantic import Field
from .common import Wire, Timestamp

class HealthResponse(Wire):
    status: Literal["ok"]
    apiVersion: str
    mode: Literal["integration_skeleton", "workspace"]
    scientificServices: Literal["unavailable"]

class AnalysisCapabilities(Wire):
    create: bool
    delete: bool
    retry: bool
    maxClaims: Annotated[int, Field(ge=1, le=10)]
    modes: list[Literal["verified", "exploratory"]]
    reviewDepths: list[Literal["focused", "council"]]

class ReadCreateCapabilities(Wire):
    read: bool
    create: bool
class ReadCapabilities(Wire):
    read: bool
class ResearchCapabilities(Wire):
    comparison: bool
    benchmarks: ReadCreateCapabilities
    reports: ReadCapabilities
    integrations: ReadCapabilities
class Provider(Wire):
    name: str
    status: Literal["configured", "not_configured", "unavailable"]
class Service(Wire):
    name: str
    status: Literal["available", "unavailable", "not_configured"]
class CapabilitiesResponse(Wire):
    providers: list[Provider]
    jobAvailability: Literal["available", "unavailable", "unknown"]
    activity: bool
    analyses: AnalysisCapabilities
    services: list[Service]
    research: ResearchCapabilities
class ActivityEvent(Wire):
    id: str
    timestamp: Timestamp
    description: str
    analysisId: NotRequired[str]
class ActivityResponse(Wire):
    items: list[ActivityEvent]
