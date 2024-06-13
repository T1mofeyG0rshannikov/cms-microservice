from domens.models import Site
from settings.models import SiteSettings
from settings.serializers import SettingsSerializer


def get_settings(subdomen: str) -> dict:
    if Site.objects.filter(domen=subdomen).exists():
        site = Site.objects.get(domen=subdomen)
        settings = SiteSettings.objects.prefetch_related("icon").prefetch_related("logo").first()
        settings = SettingsSerializer(settings).data

        if site.use_default_settings:
            return settings

        settings["logo"] = {"image": site.logo.url, "width": site.logo_width, "width_mobile": site.logo_width_mobile}

        settings["form_logo"] = {
            "image": site.logo2.url,
            "width": site.logo_width,
            "width_mobile": site.logo_width_mobile,
        }

        return settings

    settings = SiteSettings.objects.prefetch_related("icon").prefetch_related("logo").first()

    return SettingsSerializer(settings).data
