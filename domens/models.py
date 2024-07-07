from django.db import models
from django.utils import timezone

from account.models import UserFont


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
    logo = models.ImageField(verbose_name="Лого", upload_to="images/logo", null=True, blank=True)
    logo_width = models.CharField(verbose_name="ширина лого", max_length=20, null=True, blank=True)
    logo_width_mobile = models.CharField(verbose_name="ширина лого(мобильный)", max_length=20, null=True, blank=True)
    logo2 = models.ImageField(verbose_name="Лого для форм", upload_to="images/logo", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="активный", default=True)
    use_default_settings = models.BooleanField(verbose_name="Использовать общие настройки сайта", default=False)
    advertising_channel = models.CharField(verbose_name="Рекламный канал", null=True, max_length=100)
    user = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, verbose_name="пользователь", null=True, blank=True, related_name="site"
    )

    online_from = models.DateField(verbose_name="онлайн с", default=timezone.now())

    name = models.CharField(verbose_name="Название сайта", max_length=50, null=True)
    font = models.ForeignKey(UserFont, on_delete=models.SET_NULL, null=True, verbose_name="шрифт")
    font_size = models.PositiveIntegerField(verbose_name="размер шрифта", null=True)

    owner = models.CharField(max_length=150, verbose_name="Владелец", null=True)
    contact_info = models.CharField(max_length=200, verbose_name="Контактная информация", null=True)

    class Meta:
        verbose_name = "сайт"
        verbose_name_plural = "сайты партнёров"

    def __str__(self):
        return self.subdomain

    def activate(self):
        self.is_active = True
        self.online_from = timezone.now()
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    @property
    def logo_size(self):
        coeff = self.logo.height / self.logo.width

        width = int(self.logo_width)
        height = int(width * coeff)

        return f"{width}x{height}px"
