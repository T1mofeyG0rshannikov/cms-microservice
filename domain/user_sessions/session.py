from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionInterface:
    id: int
    ip: str
    start_time: datetime
    site: str
    device: bool
    pages_count: int = 0
    show_capcha: bool = False
    ban_rate: int = 0


@dataclass
class UserSessionInterface:
    ip: str
    start_time: datetime
    site: str
    device: bool
    session: SessionInterface
    banks_count: int = 0
    pages_count: int = 0
    auth: str = None
