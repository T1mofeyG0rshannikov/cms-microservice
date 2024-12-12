from dataclasses import dataclass
from datetime import datetime

from domain.user.user import UserInterface


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
    auth: str = None
    user_id: int = None
    hacking: bool = False
    headers: str = None


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
    auth: str = None
    profile_actions_count: int = 0
    user: UserInterface = None
