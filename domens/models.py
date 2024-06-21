from django.db import models

from user.models import User


class Domain(models.Model):
    domain = models.CharField(max_length=50, verbose_name="домен")
    is_partners = models.BooleanField(default=True, verbose_name="партнёрский сайт")

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = "домен"
        verbose_name_plural = "домены"


class Site(models.Model):
    domain = models.ForeignKey(Domain, verbose_name="домен", on_delete=models.CASCADE, null=True)
    subdomain = models.CharField(max_length=50, verbose_name="поддомен", unique=True)
    logo = models.ImageField(verbose_name="Лого", upload_to="images/logo")
    logo_width = models.CharField(verbose_name="ширина лого", max_length=20, null=True)
    logo_width_mobile = models.CharField(verbose_name="ширина лого(мобильный)", max_length=20, null=True)
    logo2 = models.ImageField(verbose_name="Лого для форм", upload_to="images/logo")
    is_active = models.BooleanField(verbose_name="активный", default=True)
    use_default_settings = models.BooleanField(verbose_name="Использовать общие настройки сайта", default=False)
    advertising_channel = models.CharField(verbose_name="Рекламный канал", null=True, max_length=100)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="пользователь", null=True, blank=True, related_name="site"
    )

    class Meta:
        verbose_name = "сайт"
        verbose_name_plural = "сайты партнёров"

    def __str__(self):
        return self.subdomain
