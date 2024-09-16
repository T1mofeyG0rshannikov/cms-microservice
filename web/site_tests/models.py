from django.db import models


class TestUserSet(models.Model):
    users_count = models.PositiveSmallIntegerField(verbose_name="Количество пользователей")

    def __str__(self):
        return f"Тестовый набор пользователей №{self.id}"
