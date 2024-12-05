import inspect
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawSessionDB:
    ip: str
    start_time: datetime
    site: str
    device: bool
    utm_source: str = None
    hacking: bool = False
    headers: str = None
    ban_rate: int = 0

    @classmethod
    def from_dict(cls, env: dict):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


@dataclass
class UserSessionDB:
    ip: str
    start_time: datetime
    site: str
    device: bool
    session_id: int
    banks_count: int = 0
    auth: str = None
    profile_actions_count: int = 0
    user_id: int = None


@dataclass
class SearcherDTO:
    ip: str
    start_time: datetime
    site: str
    headers: str = None
