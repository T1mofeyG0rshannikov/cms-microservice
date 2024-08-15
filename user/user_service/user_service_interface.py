from typing import Protocol

from domens.domain_service.domain_service_interface import DomainServiceInterface
from user.models import User


class UserServiceInterface(Protocol):
    domain_service: DomainServiceInterface

    def get_user_from_site(self, site, domain) -> User:
        raise NotImplementedError()

    def get_referrals_from_users(self, users: list[User]) -> list[User]:
        raise NotImplementedError()

    def get_referrals(self, user: User, level=None, sorted_by=None) -> list[User]:
        raise NotImplementedError()

    def set_referrals(self, referrals: list[User]) -> None:
        raise NotImplementedError()

    def sort_referrals(self, referrals: list[User], sorted_by: str):
        raise NotImplementedError()

    def set_referral_level(self, referrals: list[User], level: int) -> list[User]:
        raise NotImplementedError()
