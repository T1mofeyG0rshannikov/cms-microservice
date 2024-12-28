from dataclasses import dataclass
from datetime import datetime

from domain.common.screen import ImageInterface


@dataclass
class SiteLogoInterface:
    image: ImageInterface

    width_mobile: int | None | None
    width: int | None = None
    height: str | None = None
    height_mobile: str | None = None


@dataclass
class SiteSettingsInterface:
    disable_partners_sites: bool
    default_users_font_size: int
    created_at: datetime | None = None
    logo: SiteLogoInterface | None = None
    form_logo: SiteLogoInterface | None = None
    site_font: str | None = None
    icon: str | None = None
    site_font_size: int | None = None
    owner: str | None = None
    contact_info: str | None = None
