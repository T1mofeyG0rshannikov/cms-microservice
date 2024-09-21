from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web.user"
    label = "user"
    verbose_name = "Пользователи"

    def ready(self):
        import web.user.signals
