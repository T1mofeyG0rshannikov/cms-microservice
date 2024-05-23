from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="Имя пользователя", max_length=100)
    phone = models.CharField(verbose_name="Номер телефона", max_length=12)

    email = models.CharField(verbose_name="E-mail", max_length=200, null=True)
    new_email = models.CharField(verbose_name="новый E-main", max_length=200, null=True, blank=True)
    email_is_confirmed = models.BooleanField(verbose_name="Почта подтверждена", default=False)
    created_at = models.DateTimeField(verbose_name="пользователь создан", auto_now_add=True, null=True)

    USERNAME_FIELD = "id"

    def __str__(self) -> str:
        return self.username

    def verify_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def confirm_email(self) -> None:
        self.email_is_confirmed = True
        self.save()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
