from dataclasses import dataclass

from django.http import HttpRequest

from domain.user.user import UserInterface


@dataclass
class RequestUserInterface(UserInterface):
    is_authenticated: bool


@dataclass
class RequestInterface(HttpRequest):
    raw_session_id: int
    user_session_id: int
    user_from_header: UserInterface
    site_name: str
    user: RequestUserInterface
    domain: str = None
    subdomain: str = None
