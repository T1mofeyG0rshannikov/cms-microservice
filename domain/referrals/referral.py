from dataclasses import dataclass
from datetime import datetime

from domain.user.user import UserInterface
from typing import Optional


@dataclass
class ReferralInterface(UserInterface):
    level: int
    count_level_1: int
    referrals: str
    created_at: datetime
    
    sponsor: Optional['ReferralInterface']
    referrals: int