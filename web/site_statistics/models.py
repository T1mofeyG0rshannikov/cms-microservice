from django.db import models

from infrastructure.persistence.models.user.user import User
from web.common.models import OneInstanceModel


class TryLoginToAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка входа в админку"
        verbose_name_plural = "Попытки входа в админку"

    def __str__(self):
        return f"{self.date} - {self.client_ip}: {self.login}"


class TryLoginToFakeAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка входа в фейковую админку"
        verbose_name_plural = "Попытки входа в фейковую админку"

    def __str__(self):
        return f"{self.date} - {self.client_ip}: {self.login}"


class BaseSessionModel(models.Model):
    unique_key = models.CharField(unique=True, max_length=500, null=True)
    ip = models.CharField(max_length=15)
    start_time = models.DateTimeField(verbose_name="Дата")
    end_time = models.DateTimeField()
    site = models.CharField(max_length=50, null=True, verbose_name="Сайт")
    device = models.BooleanField(default=False)
    pages_count = models.PositiveIntegerField(verbose_name="Страницы", default=0)
    hacking = models.BooleanField(default=False)
    hacking_reason = models.CharField(max_length=100, null=True, blank=True)
    banks_count = models.PositiveIntegerField(verbose_name="Банки", default=0)
    profile_actions_count = models.PositiveIntegerField(verbose_name="Действия в лк", default=0)
    auth = models.CharField(null=True, max_length=20)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    utm_source = models.CharField(max_length=500, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"""{self.start_time.strftime("%d.%m.%Y")} - {self.end_time.strftime("%d.%m.%Y")}"""


class SessionModel(BaseSessionModel):
    class Meta:
        verbose_name = "Сессии"
        verbose_name_plural = "Сессии"


class UserActivity(BaseSessionModel):
    class Meta:
        verbose_name = "Посетители"
        verbose_name_plural = "Посетители"


class BaseSessionAction(models.Model):
    adress = models.CharField(max_length=300, verbose_name="страница")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-time"]
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return ""


class UserAction(BaseSessionAction):
    text = models.CharField(max_length=200, verbose_name="")
    session = models.ForeignKey(UserActivity, on_delete=models.CASCADE, null=True)


class SessionAction(BaseSessionAction):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, null=True)


class SessionFilters(OneInstanceModel):
    disable_ip = models.BooleanField(verbose_name="Запретить запросы по IP")
    disable_ports = models.BooleanField(verbose_name="Запретить обращение к нетипичным портам")
    disable_robots = models.BooleanField(verbose_name="Разрешить доступ к robots.txt только поисковкам")
    disable_urls = models.TextField(verbose_name="Запрос содержит")

    class Meta:
        verbose_name = "Фильтры сессий"
        verbose_name_plural = "Фильтры сессий"
