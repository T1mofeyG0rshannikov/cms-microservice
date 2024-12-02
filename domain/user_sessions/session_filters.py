from dataclasses import dataclass
from typing import Iterable

from domain.user_sessions.header_contain_enum import HeaderContainEnum


@dataclass
class SessionFIltersHeader:
    penalty: int
    contain: HeaderContainEnum
    content: str
    header: str

@dataclass
class SessionFilters:
    headers: Iterable[SessionFIltersHeader]