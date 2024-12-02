import inspect
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserActivityDTO:
    ip: str
    start_time: datetime
    site: str
    device: bool
    session_id: int
    banks_count: int = 0
    auth: str = None
    user_id: int = None
    profile_actions_count: int = 0
    utm_source: str = None

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


@dataclass
class RawSessionDTO:
    id: int
    ip: str
    start_time: datetime
    site: str
    device: bool
    banks_count: int = 0
    auth: str = None
    user_id: int = None
    profile_actions_count: int = 0
    utm_source: str = None
    hacking: bool = False
    headers: str = None
    ban_rate: int = 0
    show_capcha: bool = False

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


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
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


@dataclass
class SearcherDTO:
    ip: str
    start_time: datetime
    site: str
    headers: str = None
