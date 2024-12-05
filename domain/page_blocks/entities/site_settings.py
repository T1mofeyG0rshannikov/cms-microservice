from dataclasses import dataclass


@dataclass
class SiteLogoInterface:
    image: str
    width: str
    width_mobile: str

    height: str = None
    height_mobile: str = None


@dataclass
class SiteSettingsInterface:
    disable_partners_sites: bool
    default_users_font_size: int
    logo: SiteLogoInterface = None
    form_logo: SiteLogoInterface = None
    site_font: str = None
    icon: str = None
    site_font_size: str = None
    owner: str = None
    contact_info: str = None
