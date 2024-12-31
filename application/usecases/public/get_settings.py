from domain.domains.domain_repository import DomainRepositoryInterface
from domain.page_blocks.entities.site_settings import (
    SiteLogoInterface,
    SiteSettingsInterface,
)
from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from domain.user.sites.site_repository import SiteRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.page_repository import get_page_repository
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)
from infrastructure.persistence.repositories.site_repository import get_site_repository


class GetSettings:
    def __init__(
        self,
        settings_repository: SettingsRepositoryInterface,
        site_repository: SiteRepositoryInterface,
        page_repository: PageRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
    ) -> None:
        self.settings_repository = settings_repository
        self.site_repository = site_repository
        self.page_repository = page_repository
        self.domain_repository = domain_repository

    def __call__(self, domain: str | None = None, subdomain: str | None = None) -> SiteSettingsInterface:
        settings_model = self.settings_repository.get_settings()
        form_logo_model = self.settings_repository.get_form_logo()
        logo_model = self.settings_repository.get_logo()
        icon_model = self.settings_repository.get_icon()

        form_logo = SiteLogoInterface(
            image=form_logo_model.image,
            width=form_logo_model.width,
            height=form_logo_model.height,
            width_mobile=form_logo_model.width_mobile,
            height_mobile=form_logo_model.height_mobile,
        )

        logo = SiteLogoInterface(
            image=logo_model.image,
            width=logo_model.width,
            height=logo_model.height,
            width_mobile=logo_model.width_mobile,
            height_mobile=logo_model.height_mobile,
        )

        settings = SiteSettingsInterface(
            logo=logo,
            form_logo=form_logo,
            disable_partners_sites=settings_model.disable_partners_sites,
            default_users_font_size=settings_model.default_users_font_size,
            icon=icon_model.image,
        )

        if domain:
            if domain == "localhost":
                site = self.site_repository.get(subdomain=subdomain)
            else:
                site = self.site_repository.get(domain=domain, subdomain=subdomain)

            if site:
                if site.use_default_settings:
                    return settings

                settings.site_font = site.font
                settings.site_font_size = site.font_size

                if site.logo:
                    settings.logo = SiteLogoInterface(
                        image=site.logo,
                        width=site.logo_width,
                        width_mobile=site.logo_width_mobile,
                    )

                if site.logo2:
                    settings.form_logo = SiteLogoInterface(
                        image=site.logo2,
                        width=site.logo_width,
                        width_mobile=site.logo_width_mobile,
                    )

            if self.domain_repository.landing_domain_exists(domain):
                if settings.logo:
                    landing_logo = self.page_repository.get_landing_logo(domain)
                    if landing_logo:
                        settings.logo.image = landing_logo

        return settings


def get_get_settings_interactor(
    site_repository: SiteRepositoryInterface = get_site_repository(),
    settings_repository: SettingsRepositoryInterface = get_settings_repository(),
    page_repository: PageRepositoryInterface = get_page_repository(),
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
) -> GetSettings:
    return GetSettings(
        site_repository=site_repository,
        settings_repository=settings_repository,
        page_repository=page_repository,
        domain_repository=domain_repository,
    )
