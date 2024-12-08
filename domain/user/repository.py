from typing import Any, Protocol

from domain.user.user import UserInterface


class UserRepositoryInterface(Protocol):
    def get_user_by_id(self, id: int) -> UserInterface | None:
        raise NotImplementedError

    def get_supersponsor(self) -> UserInterface:
        raise NotImplementedError

    def get_user_by_phone(self, phone: str) -> UserInterface | None:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> UserInterface | None:
        raise NotImplementedError

    def verify_password(self, user_id: int, password: str) -> bool:
        raise NotImplementedError

    def create_user(self, fields: dict[str, Any]) -> UserInterface | None:
        raise NotImplementedError

    def set_password(self, user_id: int, password: str) -> UserInterface:
        raise NotImplementedError

    def change_user_email(self, user_id: int, email: str) -> None:
        raise NotImplementedError

    def update_or_create_user_messanger(self, user_id: int, messanger_id: int, adress: str) -> None:
        raise NotImplementedError

    def update_user(id: int, **kwargs) -> None:
        raise NotImplementedError
