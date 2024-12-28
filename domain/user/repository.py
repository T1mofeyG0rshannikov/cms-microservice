from typing import Protocol

from domain.common.screen import FileInterface
from domain.user.entities import UserInterface


class UserRepositoryInterface(Protocol):
    def get(
        self,
        phone: str | None = None,
        email: str | None = None,
        id: int | None = None,
        supersponsor: bool | None = None,
    ) -> UserInterface:
        raise NotImplementedError

    def verify_password(self, user_id: int, password: str) -> bool:
        raise NotImplementedError

    def create(self, email: str, phone: str, **kwargs) -> UserInterface | None:
        raise NotImplementedError

    def set_password(self, user_id: int, password: str) -> UserInterface:
        raise NotImplementedError

    def change_email(self, user_id: int, email: str) -> None:
        raise NotImplementedError

    def update_or_create_messanger(self, user_id: int, messanger_id: int, adress: str) -> None:
        raise NotImplementedError

    def update(
        self,
        id: int,
        username: str,
        second_name: str,
        phone: str,
        phone_is_confirmed: bool,
        profile_picture: FileInterface | None = None,
    ) -> None:
        raise NotImplementedError

    def confirm_phone(self, user_id: int) -> None:
        raise NotImplementedError
