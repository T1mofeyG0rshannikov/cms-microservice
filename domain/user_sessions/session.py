import inspect
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

    @classmethod
    def from_dict(cls, env: dict):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


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
