"""Development defaults, deliberately separate from legacy Flask configuration."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Settings:
    lease_seconds: float = 30
    heartbeat_seconds: float = 5
    heartbeat_timeout: float = 2
    missed_heartbeats: int = 2
    polling_seconds: float = 2
    max_attempts: int = 3
    retry_base: float = 2
    retry_cap: float = 15
    analysis_limit: int = 2
    analysis_llm_limit: int = 1
    global_llm_limit: int = 2
    provider_llm_limit: int = 2
    global_admission: int = 16
    account_admission: int = 4
    db_attempts: int = 3
    db_deadline: float = 2
    pool_timeout: float = 1
    lock_timeout_ms: int = 500
    statement_timeout_ms: int = 1000
    stop_grace: float = 2
    kill_grace: float = 2

    def __post_init__(self):
        for key,value in vars(self).items():
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or value <= 0:
                raise ValueError(f"{key} must be positive and finite")
        for key in ('missed_heartbeats','max_attempts','analysis_limit','analysis_llm_limit','global_llm_limit',
                    'provider_llm_limit','global_admission','account_admission','db_attempts','lock_timeout_ms','statement_timeout_ms'):
            if type(getattr(self,key)) is not int: raise ValueError(f"{key} must be an integer")
        if self.heartbeat_seconds >= self.lease_seconds or self.heartbeat_timeout >= self.lease_seconds:
            raise ValueError("heartbeat interval/deadline must be shorter than lease")
        if self.retry_base > self.retry_cap: raise ValueError("retry base exceeds cap")
        if self.account_admission > self.global_admission: raise ValueError("account admission exceeds global")
