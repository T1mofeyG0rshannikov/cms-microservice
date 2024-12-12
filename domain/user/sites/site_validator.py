from dataclasses import dataclass
from typing import Protocol

from domain.common.screen import FileInterface


@dataclass
class SiteValidatorInterface(Protocol):
    def valid_name(self, name: str) -> str:
        raise NotImplementedError

    def valid_site(self, site: str) -> str:
        raise NotImplementedError

    def valid_logo(self, logo: FileInterface) -> FileInterface:
        raise NotImplementedError
