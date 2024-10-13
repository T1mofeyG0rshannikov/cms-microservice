from django.db import models

from infrastructure.persistence.models.common import OneInstanceModel
from infrastructure.persistence.models.user.user import User


class TryLoginToAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "site_statistics"
        verbose_name = "Попытка входа в админку"
        verbose_name_plural = "Попытки входа в админку"

    def __str__(self):
        return f"{self.date} - {self.client_ip}: {self.login}"


class TryLoginToFakeAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "site_statistics"
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
    hacking = models.BooleanField(default=False)
    hacking_reason = models.CharField(max_length=100, null=True, blank=True)
    banks_count = models.PositiveIntegerField(verbose_name="Банки", default=0)
    profile_actions_count = models.PositiveIntegerField(verbose_name="ЛК", default=0)
    auth = models.CharField(null=True, max_length=20)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    utm_source = models.CharField(max_length=500, null=True)

    class Meta:
        abstract = True


class SessionModel(BaseSessionModel):
    headers = models.TextField(max_length=2000, null=True)
    ban_rate = models.SmallIntegerField(default=0, verbose_name="Штраф")

    class Meta:
        app_label = "site_statistics"
        verbose_name = "Сессии"
        verbose_name_plural = "Сессии"

    def __str__(self):
        return f"{self.site} - {self.ip}"


class UserActivity(BaseSessionModel):
    class Meta:
        app_label = "site_statistics"
        verbose_name = "Посетители"
        verbose_name_plural = "Посетители"


class BaseSessionAction(models.Model):
    adress = models.CharField(max_length=300, verbose_name="страница")
    time = models.DateTimeField()

    class Meta:
        abstract = True
        ordering = ["-time"]
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return ""


class UserAction(BaseSessionAction):
    text = models.CharField(max_length=200, verbose_name="")
    session = models.ForeignKey(UserActivity, on_delete=models.CASCADE, null=True, related_name="actions")
    is_page = models.BooleanField(default=True)

    class Meta:
        ordering = ["-time"]
        app_label = "site_statistics"

        indexes = [
            models.Index(
                fields=[
                    "session_id",
                ]
            )
        ]


class SessionAction(BaseSessionAction):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, null=True, related_name="actions")
    is_page = models.BooleanField(default=True)
    is_source = models.BooleanField(default=False)

    @property
    def last_action(self):
        last_action = self.actions.first()
        if last_action:
            return last_action.time

    class Meta:
        app_label = "site_statistics"
        ordering = ["-time"]

        indexes = [
            models.Index(
                fields=[
                    "session_id",
                ]
            )
        ]


class SessionFilters(OneInstanceModel):
    searchers = models.TextField(verbose_name="Поисковики", null=True)
    capcha_limit = models.SmallIntegerField(verbose_name="Порог капчи", default=10000)
    ban_limit = models.SmallIntegerField(verbose_name="Порог бана", default=10000)

    ip_penalty = models.SmallIntegerField(verbose_name="Запрос к IP", default=0)
    ports_penalty = models.SmallIntegerField(verbose_name="Запрос к порту", default=0)
    disable_urls = models.TextField(verbose_name="Запрос содержит")
    disable_urls_penalty = models.SmallIntegerField("Запрещенный адрес", default=0)
    page_not_found_penalty = models.SmallIntegerField("Несуществующий адрес", default=0)

    reject_capcha = models.SmallIntegerField(verbose_name="Отказ от капчи", default=0)
    capcha_error = models.SmallIntegerField(verbose_name="Ошибка в капче", default=0)

    capcha_success = models.SmallIntegerField(verbose_name="Успешная капча", default=0)

    class Meta:
        app_label = "site_statistics"
        verbose_name = "Фильтры сессий"
        verbose_name_plural = "Фильтры сессий"


class SessionFiltersHeader(models.Model):
    session_filters = models.ForeignKey(SessionFilters, on_delete=models.CASCADE, related_name="headers")
    header = models.CharField(max_length=50, verbose_name="Заголовок")
    CONTAIN_CHOICES = [
        ("Присутствует", "Присутствует"),
        ("Отсутствует", "Отсутствует"),
        ("Содержит", "Содержит"),
        ("Не содержит", "Не содержит"),
        ("Совпадает", "Совпадает"),
        ("Не совпадает", "Не совпадает"),
    ]

    contain = models.CharField(max_length=50, choices=CONTAIN_CHOICES, verbose_name="содержит")
    content = models.CharField(max_length=50, null=True, blank=True, verbose_name="строка")
    penalty = models.SmallIntegerField(default=0, verbose_name="штраф")

    class Meta:
        app_label = "site_statistics"


class PenaltyLog(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    class Meta:
        app_label = "site_statistics"
