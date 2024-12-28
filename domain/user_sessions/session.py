from dataclasses import dataclass
from datetime import datetime

from domain.user.entities import UserInterface


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
    banks_count: int = 0
    auth: str | None = None
    user_id: int | None = None
    hacking: bool = False
    headers: str | None = None


@dataclass
class UserSessionInterface:
    id: int
    ip: str
    start_time: datetime
    site: str
    device: bool
    session: SessionInterface
    banks_count: int = 0
    pages_count: int = 0
    auth: str | None = None
    profile_actions_count: int = 0
    user: UserInterface | None = None
