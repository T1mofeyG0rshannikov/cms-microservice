from .models import SiteSettings
from .serializers import SettingsSerializer


def get_settings():
    settings = SiteSettings.objects.first()

    settings = SettingsSerializer(settings).data

    return settings
