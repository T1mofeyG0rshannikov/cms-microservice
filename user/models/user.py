from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from domens.domain_service.domain_service import get_domain_service
from user.models.site import Site
from user.user_manager.user_manager import UserManager
from user.user_manager.user_manager_interface import UserManagerInterface


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="Имя пользователя", max_length=100)
    second_name = models.CharField(verbose_name="Фамлия", max_length=200, null=True, blank=True)

    phone = models.CharField(verbose_name="Номер телефона", max_length=12, null=True)
    phone_is_confirmed = models.BooleanField(verbose_name="Телефон подтвержден", default=False)

    email = models.CharField(verbose_name="E-mail", max_length=200, null=True)
    new_email = models.CharField(verbose_name="новый E-main", max_length=200, null=True, blank=True)
    email_is_confirmed = models.BooleanField(verbose_name="Почта подтверждена", default=False)

    created_at = models.DateTimeField(verbose_name="пользователь создан", auto_now_add=True, null=True)

    profile_picture = models.ImageField(verbose_name="аватарка", null=True, blank=True)

    register_on_site = models.ForeignKey(
        Site,
        verbose_name="зарегистрирован на сайте",
        related_name="register_on_site",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    register_on_domain = models.ForeignKey(
        "settings.Domain",
        verbose_name="зарегистрирован на домене",
        related_name="register_on_domain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "id"

    staff = models.BooleanField(default=False)

    objects: UserManagerInterface = UserManager()

    supersponsor = models.BooleanField(verbose_name="Главный спонсор", default=False)

    sponsor = models.ForeignKey(
        "self", verbose_name="Спонсор", null=True, blank=True, on_delete=models.SET_NULL, related_name="sponsors"
    )

    test = models.BooleanField(default=False, verbose_name="тестовый пользователь")

    test_set = models.ForeignKey("site_tests.TestUserSet", null=True, blank=True, on_delete=models.CASCADE)

    @property
    def is_staff(self):
        return self.staff

    @property
    def full_site_name(self) -> str | None:
        if Site.objects.filter(user_id=self.id).exists():
            return f"{self.site}.{get_domain_service().get_partners_domain_string()}"

        return None

    @property
    def full_name(self) -> str:
        full_name = self.username
        if self.second_name:
            full_name += " " + self.second_name

        return full_name

    def __str__(self) -> str:
        return self.full_name

    def verify_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def confirm_email(self) -> None:
        self.email_is_confirmed = True
        self.save()

    def change_email(self, new_email: str) -> None:
        if self.email_is_confirmed:
            self.new_email = new_email

        else:
            self.email = new_email

        self.save()

    def confirm_new_email(self) -> None:
        self.email = self.new_email
        self.new_email = None
        self.email_is_confirmed = True
        self.save()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        indexes = [
            models.Index(
                fields=[
                    "sponsor_id",
                ]
            )
        ]
