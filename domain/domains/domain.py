from dataclasses import dataclass


@dataclass
class DomainInterface:
    domain: str
    is_partners: bool
    name: str | None = None
