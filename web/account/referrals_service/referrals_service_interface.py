from typing import Protocol

from domain.user.interfaces import UserInterface


class ReferralServiceInterface(Protocol):
    total_referal_level: int

    def get_referral_level(self, referral: UserInterface, user: UserInterface):
        raise NotImplementedError()

    def get_referral(self, user_id: int, user: UserInterface):
        raise NotImplementedError()

    def set_referrals_count(self, referrals) -> list[UserInterface]:
        raise NotImplementedError()

    def set_referral_level(self, referrals: list[UserInterface], level: int) -> list[UserInterface]:
        raise NotImplementedError()

    def get_referrals(self, user: UserInterface, level=None, sorted_by=None) -> list[UserInterface]:
        raise NotImplementedError()
