from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.models.settings import (
    FormLogo,
    Icon,
    Logo,
    SiteSettings,
)


class SettingsRepository(SettingsRepositoryInterface):
    def get_settings(self):
        return SiteSettings.objects.first()

    def get_form_logo(self):
        return FormLogo.objects.first()

    def get_logo(self):
        return Logo.objects.first()

    def get_icon(self):
        return Icon.objects.first()


def get_settings_repository() -> SettingsRepositoryInterface:
    return SettingsRepository()
