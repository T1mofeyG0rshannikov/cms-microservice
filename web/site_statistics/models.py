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


class TryLoginToFakeAdminPanel(models.Model):
    client_ip = models.CharField(max_length=15, verbose_name="ip с которого был запрос")
    login = models.CharField(max_length=100, verbose_name="логин")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка входа в фейковую админку"
        verbose_name_plural = "Попытки входа в фейковую админку"

    def __str__(self):
        return f"{self.date} - {self.client_ip}: {self.login}"


class UserActivity(models.Model):
    unique_key = models.CharField(unique=True, max_length=500, null=True)
    ip = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    banks_count = models.PositiveIntegerField(default=0)
    pages_count = models.PositiveIntegerField(default=0)
    popups_count = models.PositiveIntegerField(default=0)
    auth = models.CharField(null=True, max_length=20)

    def __str__(self):
        return f"""{self.start_time.strftime("%d.%m.%Y")} - {self.end_time.strftime("%d.%m.%Y")}"""

    class Meta:
        verbose_name = "Посетители"
        verbose_name_plural = "Посетители"


class GoToThePage(models.Model):
    session = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    url = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Переходы по страницам"
        verbose_name = "страница"
        ordering = ["-id"]

    def __str__(self):
        return ""


class UserAction(models.Model):
    session = models.ForeignKey(UserActivity, on_delete=models.CASCADE, null=True)
    adress = models.CharField(max_length=300, verbose_name="страница")
    text = models.CharField(max_length=200, verbose_name="")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return ""
