from dataclasses import dataclass

from domain.domains.domain import DomainInterface
from domain.user.sites.site import SiteInterface


@dataclass
class UserInterface:
    pk: int
    id: int
    username: str
    second_name: str
    full_name: str

    phone: str
    phone_is_confirmed: bool

    email: str
    new_email: str
    email_is_confirmed: bool

    password: str | None

    site: SiteInterface | None

    register_on_site: SiteInterface | None
    register_on_domain: DomainInterface | None

    is_superuser: bool
    profile_picture: str

    def check_password(self, password: str):
        pass

    def set_password(self, password: str):
        pass

    def confirm_email(self) -> None:
        pass
