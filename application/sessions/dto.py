from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawSessionDB:
    ip: str
    start_time: datetime
    site: str
    device: bool
    hacking: bool = False
    utm_source: str | None = None
    headers: str | None = None
    ban_rate: int = 0


@dataclass
class UserSessionDB:
    start_time: datetime
    session_id: int
    banks_count: int = 0
    auth: str | None = None
    profile_actions_count: int = 0
    user_id: int | None = None


@dataclass
class SearcherDTO:
    ip: str
    start_time: datetime
    site: str
    headers: str | None = None
