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
    ip_penalty: int
    ports_penalty: int
    disable_urls: str
    disable_urls_penalty: int
    disable_urls_sites: str
    ban_limit: int
    capcha_limit: int
    page_not_found_penalty: int
    reject_capcha: int
