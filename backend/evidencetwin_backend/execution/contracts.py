"""Internal execution contracts, never public scientific/API verdicts."""
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
import re
from typing import Any, Protocol
from uuid import UUID

class JobState(StrEnum):
    QUEUED='queued'; RUNNING='running'; RETRY_WAIT='retry_wait'
    RECONCILIATION='reconciliation_required'; CANCELLING='cancellation_requested'
    SUCCEEDED='succeeded'; FAILED='failed'; CANCELLED='cancelled'

class AttemptState(StrEnum):
    PENDING='pending'; RUNNING='running'; CANCELLING='cancellation_requested'
    SUCCEEDED='succeeded'; FAILED='failed'; ABANDONED='abandoned'; CANCELLED='cancelled'

class Rejected(Exception):
    """Only safe machine codes may be returned to callers."""
    def __init__(self, code='guard_rejected'):
        self.code=code if isinstance(code,str) and re.fullmatch(r'[a-z][a-z0-9_]{0,63}',code) else 'internal_execution_error'
        super().__init__(self.code)
class Conflict(Rejected): pass
class CapacityUnavailable(Rejected): pass
class IntegrationUnavailable(Rejected): pass
class Contention(Rejected): pass
class CommitUnknown(Rejected): pass

@dataclass(frozen=True)
class Principal:
    owner_ref: str
    actor_ref: str
    roles: frozenset[str] = field(default_factory=frozenset)
    def __post_init__(self):
        if any(not isinstance(v,str) or not v or len(v)>512 for v in (self.owner_ref,self.actor_ref)):
            raise ValueError('invalid principal reference')

@dataclass(frozen=True)
class Lease:
    job_id: UUID
    attempt_id: UUID
    owner_instance: UUID
    fence: int
    job_version: int
    attempt_version: int
    snapshot_id: UUID
    def command(self):
        return {k:str(v) if isinstance(v,UUID) else v for k,v in vars(self).items()}
    @classmethod
    def restore(cls, data):
        return cls(**{k:UUID(v) if k.endswith('_id') or k=='owner_instance' else v for k,v in data.items()})

@dataclass(frozen=True)
class StopProof:
    instance: UUID
    evidence_ref: str

class Authorizer(Protocol):
    def authorize(self, principal: Principal, action: str, snapshot: dict) -> bool: ...
class Validator(Protocol):
    def validate(self, payload: bytes, snapshot: dict, kind: str) -> bytes: ...
class ArtifactVerifier(Protocol):
    def ready(self, artifact: dict, snapshot: dict) -> bool: ...
class StopVerifier(Protocol):
    def stopped(self, proof: StopProof, attempt: dict) -> bool: ...

@dataclass(frozen=True)
class Adapters:
    authorizer: Authorizer | None = None
    validator: Validator | None = None
    artifacts: ArtifactVerifier | None = None
    stop: StopVerifier | None = None
    settlement: Any = None
    spend: Any = None

    def authorize(self, principal, action, snapshot):
        if self.authorizer is None: raise IntegrationUnavailable('authorizer_unavailable')
        if (action!='claim' and principal.owner_ref != snapshot['owner_ref']) or not self.authorizer.authorize(principal,action,snapshot):
            raise Rejected('access_denied')


def canonical(value: Any) -> bytes:
    def validate(v):
        if v is None or type(v) in (bool,int): return
        if isinstance(v,str):
            if len(v)>262144: raise Rejected('command_too_large')
            return
        if isinstance(v,list):
            for x in v: validate(x)
            return
        if isinstance(v,dict) and all(isinstance(k,str) for k in v):
            for x in v.values(): validate(x)
            return
        raise Rejected('noncanonical_value')
    try:
        validate(value)
        result=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    except (RecursionError,UnicodeError,ValueError,TypeError): raise Rejected('invalid_command') from None
    if not 0<len(result)<=262144: raise Rejected('command_too_large')
    return result

def digest(value: bytes) -> bytes: return sha256(value).digest()
