from dataclasses import dataclass
from datetime import datetime

from domain.user.user import UserInterface


@dataclass
class ReferralInterface(UserInterface):
    level: int
    first_level_referrals: int
    referrals: str
    created_at: datetime
