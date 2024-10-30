from typing import Protocol

from domain.page_blocks.site_settings import SiteLogoInterface, SiteSettingsInterface


class SettingsRepositoryInterface(Protocol):
    def get_settings(self) -> SiteSettingsInterface:
        raise NotImplementedError

    def get_form_logo(self) -> SiteLogoInterface:
        raise NotImplementedError

    def get_logo(self) -> SiteLogoInterface:
        raise NotImplementedError

    def get_icon(self):
        raise NotImplementedError
