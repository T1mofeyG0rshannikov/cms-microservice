from dataclasses import dataclass
from datetime import datetime

from domens.interfaces import DomainInterface, SiteInterface


@dataclass
class UserInterface:
    id: int
    username: str
    second_name: str

    phone: str
    phone_is_confirmed: bool

    email: str
    new_email: str
    email_is_confirmed: str

    site: SiteInterface | None

    register_on_site: SiteInterface | None
    register_on_domain: DomainInterface | None


@dataclass
class ReferralInterface(UserInterface):
    level: int
    first_level_referrals: int
    referrals: str
    created_at: datetime
