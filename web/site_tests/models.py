from django.db import models

from web.common.models import OneInstanceModel


class TestUserSet(models.Model):
    users_count = models.PositiveSmallIntegerField(verbose_name="Количество пользователей")

    def __str__(self):
        return f"Тестовый набор пользователей №{self.id}"


class Error(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name="время")
    status = models.SmallIntegerField(verbose_name="статус", null=True)
    message = models.TextField(max_length=10000, verbose_name="сообщение об ошибке")
    path = models.CharField(max_length=200, verbose_name="страница")


class EnableErrorLogging(OneInstanceModel):
    enable_error_logging = models.BooleanField(default=False, verbose_name="логировать ошибки")

    class Meta:
        app_label = "site_tests"
