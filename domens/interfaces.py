from dataclasses import dataclass


@dataclass
class DomainInterface:
    domain: str
    is_partners: bool


@dataclass
class SiteInterface:
    domain: DomainInterface
    subdomain: str
    is_active: bool
    use_default_settings: bool
    advertising_channel: str

    name: str
    owner: str
    contact_info: str
