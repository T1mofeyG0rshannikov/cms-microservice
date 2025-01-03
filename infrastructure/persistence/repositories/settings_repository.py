from collections.abc import Iterable

from domain.account.social_network import SocialNetworkInterface
from domain.domains.domain import DomainInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.models.settings import (
    Domain,
    FormLogo,
    Icon,
    Logo,
    Messanger,
    SiteSettings,
    SocialNetwork,
    UserFont,
)


class SettingsRepository(SettingsRepositoryInterface):
    def get_settings(self):
        return SiteSettings.objects.prefetch_related("logo", "form_logo", "icon").first()

    def get_form_logo(self):
        return FormLogo.objects.first()

    def get_logo(self):
        return Logo.objects.first()

    def get_icon(self):
        return Icon.objects.first()

    def get_messangers(self):
        return Messanger.objects.select_related("social_network").all()

    def get_user_fonts(self):
        return UserFont.objects.all()

    def get_social_networks(self) -> Iterable[SocialNetworkInterface]:
        return SocialNetwork.objects.all()

    def get_partner_domains(self) -> Iterable[DomainInterface]:
        return Domain.objects.values("domain", "id").filter(is_partners=True)


def get_settings_repository() -> SettingsRepositoryInterface:
    return SettingsRepository()
