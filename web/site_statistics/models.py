from django.db import models


class TryLoginToAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка входа в админку"
        verbose_name_plural = "Попытки входа в админку"

    def __str__(self):
        return f"{self.date} - {self.client_ip}: {self.login}"
