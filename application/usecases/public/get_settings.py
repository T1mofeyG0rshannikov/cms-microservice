from domain.domains.domain_repository import DomainRepositoryInterface
from domain.page_blocks.entities.site_settings import (
    SiteLogoInterface,
    SiteSettingsInterface,
)
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.models.user.site import Site
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)


class GetSettings:
    def __init__(
        self, settings_repository: SettingsRepositoryInterface, domain_repository: DomainRepositoryInterface
    ) -> None:
        self.settings_repository = settings_repository
        self.domain_repository = domain_repository

    def __call__(self, domain: str = None, subdomain: str = None) -> dict:
        settings_model = self.settings_repository.get_settings()
        form_logo_model = self.settings_repository.get_form_logo()
        logo_model = self.settings_repository.get_logo()
        icon_model = self.settings_repository.get_icon()

        form_logo = SiteLogoInterface(
            image=form_logo_model.image.url,
            width=form_logo_model.width,
            height=form_logo_model.height,
            width_mobile=form_logo_model.width_mobile,
            height_mobile=form_logo_model.height_mobile,
        )

        logo = SiteLogoInterface(
            image=logo_model.image.url,
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
            icon=icon_model.image.url,
        )

        if domain:
            sites = self.domain_repository.get_domain_sites(domain)
            sites = Site.objects.all() if domain == "localhost" else Site.objects.filter(domain__domain=domain)

            if sites.filter(subdomain=subdomain).exists():
                site = sites.get(subdomain=subdomain)

                if site.use_default_settings:
                    return settings

                settings.site_font = site.font
                settings.site_font_size = site.font_size

                if site.logo:
                    settings.logo = SiteLogoInterface(
                        image=site.logo.url,
                        width=site.logo_width,
                        width_mobile=site.logo_width_mobile,
                    )

                if site.logo2:
                    settings.form_logo = SiteLogoInterface(
                        image=site.logo2.url,
                        width=site.logo_width,
                        width_mobile=site.logo_width_mobile,
                    )

        return settings


def get_get_settings_interactor(
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    settings_repository: SettingsRepositoryInterface = get_settings_repository(),
) -> GetSettings:
    return GetSettings(domain_repository=domain_repository, settings_repository=settings_repository)
