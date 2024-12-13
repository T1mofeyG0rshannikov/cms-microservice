from typing import Protocol

from domain.user.user import UserInterface


class UserRepositoryInterface(Protocol):
    def get(self, id: int = None, phone: str = None, email: str = None) -> UserInterface | None:
        raise NotImplementedError

    def verify_password(self, user_id: int, password: str) -> bool:
        raise NotImplementedError

    def create(self, email: str, phone: str) -> UserInterface | None:
        raise NotImplementedError

    def set_password(self, user_id: int, password: str) -> UserInterface:
        raise NotImplementedError

    def change_email(self, user_id: int, email: str) -> None:
        raise NotImplementedError

    def update_or_create_messanger(self, user_id: int, messanger_id: int, adress: str) -> None:
        raise NotImplementedError

    def update(self, id: int, **kwargs) -> None:
        raise NotImplementedError

    def confirm_phone(self, user_id: int) -> None:
        raise NotImplementedError
