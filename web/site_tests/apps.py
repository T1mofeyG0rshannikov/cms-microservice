from django.apps import AppConfig


class SiteTestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.site_tests"

    verbose_name = "Отладка"

    def ready(self):
        import web.site_tests.signals
