from settings.models import SiteSettings
from settings.serializers import SettingsSerializer


def get_settings() -> dict:
    settings = SiteSettings.objects.prefetch_related("icon").prefetch_related("logo").first()

    return SettingsSerializer(settings).data
