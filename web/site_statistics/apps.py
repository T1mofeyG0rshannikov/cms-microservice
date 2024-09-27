from django.apps import AppConfig


class SiteStatisticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.site_statistics"

    verbose_name = "СТАТИСТИКА"

    def ready(self) -> None:
        import web.site_statistics.signals
