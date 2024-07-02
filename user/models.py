from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from domens.models import Domain
from user.user_manager.user_manager import UserManager
from user.user_manager.user_manager_interface import UserManagerInterface


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="Имя пользователя", max_length=100)
    phone = models.CharField(verbose_name="Номер телефона", max_length=12)

    email = models.CharField(verbose_name="E-mail", max_length=200, null=True)
    new_email = models.CharField(verbose_name="новый E-main", max_length=200, null=True, blank=True)
    email_is_confirmed = models.BooleanField(verbose_name="Почта подтверждена", default=False)
    created_at = models.DateTimeField(verbose_name="пользователь создан", auto_now_add=True, null=True)

    register_on_site = models.ForeignKey(
        "domens.Site",
        verbose_name="зарегистрирован на сайте",
        related_name="register_on_site",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    register_on_domain = models.ForeignKey(
        "domens.Domain",
        verbose_name="зарегистрирован на домене",
        related_name="register_on_domain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "id"

    staff = models.BooleanField(default=False)

    objects: UserManagerInterface = UserManager()

    @property
    def is_staff(self):
        return self.staff

    @property
    def full_site_name(self):
        return f"{self.site}.{Domain.objects.filter(is_partners=True).first().domain}"

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
