from collections.abc import Iterable
from dataclasses import dataclass

from domain.user_sessions.header_contain_enum import HeaderContainEnum


@dataclass
class SessionFIltersHeader:
    penalty: int
    contain: HeaderContainEnum
    content: str
    header: str


@dataclass
class SessionFiltersInterface:
    headers: Iterable[SessionFIltersHeader]
