from typing import Protocol

from user.models.user import User


class UserRepositoryInterface(Protocol):
    @staticmethod
    def get_user_by_id(id: int) -> User | None:
        raise NotImplementedError()

    @staticmethod
    def get_supersponsor() -> User:
        raise NotImplementedError()

    @staticmethod
    def get_referrals_by_level(sponsor: User, level: int) -> list[User]:
        raise NotImplementedError()
