from dataclasses import dataclass
from datetime import datetime

from domain.user.entities import UserInterface


@dataclass
class ReferralInterface(UserInterface):
    level: int
    count_level_1: int
    created_at: datetime

    sponsor: "ReferralInterface"
    referrals: int
