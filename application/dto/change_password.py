from dataclasses import dataclass

from domain.user.entities import UserInterface


@dataclass
class ChangePasswordResponse:
    user: UserInterface
    access_token: str
    refresh_token: str
