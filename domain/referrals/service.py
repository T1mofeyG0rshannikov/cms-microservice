from typing import Protocol

from domain.referrals.referral import ReferralInterface
from domain.user.user import UserInterface


class ReferralServiceInterface(Protocol):
    total_referal_level: int

    def get_referral_level(self, referral: UserInterface, user: UserInterface):
        raise NotImplementedError

    def get_referral(self, user_id: int, user: UserInterface):
        raise NotImplementedError

    def set_referral_level(self, referrals: list[UserInterface], level: int) -> list[ReferralInterface]:
        raise NotImplementedError

    def get_referrals(self, user_id: int, level=None, sorted_by=None) -> list[ReferralInterface]:
        raise NotImplementedError
