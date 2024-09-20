from dataclasses import dataclass

from domain.domains.domain import DomainInterface, SiteInterface


@dataclass
class UserInterface:
    id: int
    username: str
    second_name: str

    phone: str
    phone_is_confirmed: bool

    email: str
    new_email: str
    email_is_confirmed: bool

    site: SiteInterface | None

    register_on_site: SiteInterface | None
    register_on_domain: DomainInterface | None

    is_superuser: bool
