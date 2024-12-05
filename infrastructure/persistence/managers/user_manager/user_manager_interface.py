from typing import Protocol

from domain.user.user import UserInterface


class UserManagerInterface(Protocol):
    def get_user_by_email(self, email: str) -> UserInterface:
        raise NotImplementedError

    def get_user_by_phone(self, phone: str) -> UserInterface:
        raise NotImplementedError

    def create_user(self, username: str, phone: str, email: str, **extra_fields) -> UserInterface:
        raise NotImplementedError

    def get_user_by_id(self, id: int) -> UserInterface:
        raise NotImplementedError

    def filter(*args, **kwargs):
        raise NotImplementedError

    def exclude(*args, **kwargs):
        raise NotImplementedError

    def get(*args, **kwargs):
        raise NotImplementedError

    def count(*args, **kwargs):
        raise NotImplementedError
