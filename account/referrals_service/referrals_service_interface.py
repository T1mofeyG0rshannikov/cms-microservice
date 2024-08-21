from typing import Protocol

from user.interfaces import UserInterface
from user.models.user import User


class ReferralServiceInterface(Protocol):
    total_referal_level: int

    def get_referral_level(self, referral: User, user: User):
        raise NotImplementedError()

    def get_referral(self, user_id: int, user: UserInterface):
        raise NotImplementedError()

    def get_referrals_count(self, level, referral) -> int:
        raise NotImplementedError()

    def set_referrals_count(self, referrals) -> list[User]:
        raise NotImplementedError()

    def get_referrals_by_level(self, sponsor, level):
        raise NotImplementedError()

    def set_referral_level(self, referrals: list[User], level: int) -> list[User]:
        raise NotImplementedError()

    def get_referrals(self, user: User, level=None, sorted_by=None) -> list[User]:
        raise NotImplementedError()
