from dataclasses import dataclass

from domain.common.screen import FileInterface


@dataclass
class SocialNetworkInterface:
    name: str
    domain: str
    icon: FileInterface
    button_color: str
