from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserSessionInterface:
    ip: str
    start_time: datetime
    site: str
    device: bool
    banks_count: int = 0
    pages_count: int = 0
    auth: str = None


@dataclass
class SessionInterface:
    def save() -> None:
        pass
