"""AI configuration boundary. Response DTOs deliberately have no credential field."""
from typing import Annotated, Literal, NotRequired
from pydantic import StringConstraints, Field
from .common import Wire

ProviderID = Literal['ollama','openai','google','anthropic','openrouter','deepseek']
class AISettingsInput(Wire):
    provider: ProviderID
    model: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    apiKey: NotRequired[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4096, pattern=r'^[^\r\n]+$')]]
    removeKey: NotRequired[bool]
    ollamaHost: NotRequired[Annotated[str, Field(max_length=2000)]]
class AIProviderPublic(Wire):
    id: ProviderID
    name: str
    model: str
    configured: bool
    keyConfigured: bool
    keySource: Literal['server','environment','none']
    requiresKey: bool
    ollamaHost: NotRequired[str]
class AISettingsPublic(Wire):
    activeProvider: ProviderID
    providers: list[AIProviderPublic]
