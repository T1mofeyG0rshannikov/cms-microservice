from typing import Protocol

from domain.user.user import UserInterface


class UserRepositoryInterface(Protocol):
    def get_user_by_id(self, id: int) -> UserInterface | None:
        raise NotImplementedError

    def get_supersponsor(self) -> UserInterface:
        raise NotImplementedError

    def get_referrals_by_level(self, sponsor_id: int, level: int) -> list[UserInterface]:
        raise NotImplementedError

    def get_user_by_phone(self, phone: str) -> UserInterface | None:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> UserInterface | None:
        raise NotImplementedError
