from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="Имя пользователя", max_length=100)
    phone = models.CharField(verbose_name="Номер телефона", max_length=12)

    email = models.CharField(verbose_name="E-main", max_length=200)
    new_email = models.CharField(verbose_name="новый E-main", max_length=200)
    email_is_confirmed = models.BooleanField(verbose_name="Почта подтверждена", default=False)

    USERNAME_FIELD = "id"

    def __str__(self) -> str:
        return self.username
