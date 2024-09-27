from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserActivityDTO:
    unique_key: str
    ip: str
    start_time: datetime
    end_time: datetime
    site: str
    device: bool
    banks_count: int = 0
    pages_count: int = 0
    auth: str = None
    user_id: int = None
    profile_actions_count: int = 0
    utm_source: str = None
    hacking: bool = False
    hacking_reason: str = None


@dataclass
class RawSessionDTO:
    unique_key: str
    ip: str
    start_time: datetime
    end_time: datetime
    site: str
    device: bool
    banks_count: int = 0
    pages_count: int = 0
    source_count: int = 0
    auth: str = None
    user_id: int = None
    profile_actions_count: int = 0
    utm_source: str = None
    hacking: bool = False
    hacking_reason: str = None
