from dataclasses import dataclass

from domain.domains.site import DomainInterface, SiteInterface


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

    site: SiteInterface | None

    register_on_site: SiteInterface | None
    register_on_domain: DomainInterface | None

    is_superuser: bool
    profile_picture: str

    def check_password(self, password: str):
        pass
