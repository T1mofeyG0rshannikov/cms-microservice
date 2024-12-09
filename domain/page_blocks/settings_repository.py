from typing import Protocol

from collections.abc import Iterable

from domain.account.social_network import SocialNetworkInterface
from domain.domains.entities.domain import DomainInterface
from domain.page_blocks.entities.site_settings import (
    SiteLogoInterface,
    SiteSettingsInterface,
)


class SettingsRepositoryInterface(Protocol):
    def get_settings(self) -> SiteSettingsInterface:
        raise NotImplementedError

    def get_form_logo(self) -> SiteLogoInterface:
        raise NotImplementedError

    def get_logo(self) -> SiteLogoInterface:
        raise NotImplementedError

    def get_icon(self):
        raise NotImplementedError

    def get_messangers(self):
        raise NotImplementedError

    def get_user_fonts(self):
        raise NotImplementedError

    def get_social_networks(self) -> Iterable[SocialNetworkInterface]:
        raise NotImplementedError

    def get_partner_domains(self) -> Iterable[DomainInterface]:
        raise NotImplementedError
