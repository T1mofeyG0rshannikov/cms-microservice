from typing import Protocol

from domain.user.interfaces import UserInterface


class UserRepositoryInterface(Protocol):
    @staticmethod
    def get_user_by_id(id: int) -> UserInterface | None:
        raise NotImplementedError()

    @staticmethod
    def get_supersponsor() -> UserInterface:
        raise NotImplementedError()

    @staticmethod
    def get_referrals_by_level(sponsor_id: int, level: int) -> list[UserInterface]:
        raise NotImplementedError()

    @staticmethod
    def get_user_by_phone(phone: str) -> UserInterface | None:
        raise NotImplementedError()

    @staticmethod
    def get_user_by_email(email: str) -> UserInterface | None:
        raise NotImplementedError()
