from colorfield.fields import ColorField
from django.db import models

from infrastructure.persistence.models.common import BaseFont, OneInstanceModel

FONT_SIZES = (
    (6, 6),
    (8, 8),
    (9, 9),
    (10, 10),
    (12, 12),
    (14, 14),
    (18, 18),
    (24, 24),
    (30, 30),
    (36, 36),
    (48, 48),
    (60, 60),
    (72, 72),
)


class SiteSettings(OneInstanceModel):
    disable_partners_sites = models.BooleanField(default=False, verbose_name="Отключить партнёрский домен")
    default_users_font_size = models.PositiveSmallIntegerField(
        null=True, choices=FONT_SIZES, verbose_name="Размер пользовательского шрифта по умолчанию"
    )

    owner = models.CharField(max_length=150, verbose_name="Владелец", null=True)
    contact_info = models.CharField(max_length=200, verbose_name="Контактная информация", null=True)

    created_at = models.DateTimeField(verbose_name="сайт создан", auto_now_add=True, null=True)

    class Meta:
        app_label = "settings"
        verbose_name = "Айдентика"
        verbose_name_plural = "Айдентика"


class BaseLogo(OneInstanceModel):
    image = models.ImageField(verbose_name="Изображение", upload_to="images/logo")
    width = models.CharField(verbose_name="Ширина", max_length=20)
    height = models.CharField(verbose_name="Высота", max_length=20)

    width_mobile = models.CharField(verbose_name="Ширина(смартфон)", max_length=20)
    height_mobile = models.CharField(verbose_name="Высота(смартфон)", max_length=20)

    class Meta:
        abstract = True


class Logo(BaseLogo):
    settings = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name="logo")

    class Meta:
        app_label = "settings"
        verbose_name = "Логотип"
        verbose_name_plural = "Логотип"

    def save(self, *args, **kwargs):
        try:
            this = Logo.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass
        super().save(*args, **kwargs)


class FormLogo(BaseLogo):
    settings = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name="form_logo")

    class Meta:
        app_label = "settings"
        verbose_name = "Логотип для форм"
        verbose_name_plural = "Логотип для форм"

    def save(self, *args, **kwargs):
        try:
            this = FormLogo.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass
        super().save(*args, **kwargs)


class Icon(OneInstanceModel):
    image = models.ImageField(verbose_name="Изображение", upload_to="images/icon")

    settings = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name="icon")

    class Meta:
        app_label = "settings"
        verbose_name = "Иконка"
        verbose_name_plural = "Иконка"


class Domain(models.Model):
    domain = models.CharField(max_length=50, verbose_name="домен")
    is_partners = models.BooleanField(default=True, verbose_name="партнёрский сайт")
    name = models.CharField(max_length=50, verbose_name="Название", null=True, blank=True)

    def __str__(self):
        return self.domain

    class Meta:
        app_label = "settings"
        verbose_name = "домен"
        verbose_name_plural = "домены"


class GlobalStyles(OneInstanceModel):
    class Meta:
        app_label = "settings"
        verbose_name = "стили"
        verbose_name_plural = "стили"


class Font(BaseFont):
    class Meta:
        app_label = "settings"
        verbose_name = "Шрифт"
        verbose_name_plural = "Шрифты"
        ordering = ["name"]


class SocialNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    domain = models.CharField(max_length=100, verbose_name="Домен")

    icon = models.ImageField(upload_to="images/social/icons/", verbose_name="иконка")
    button_color = ColorField(verbose_name="Цвет кнопки")

    class Meta:
        app_label = "settings"
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

    def __str__(self):
        return self.name


class Messanger(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE, verbose_name="Соц. сеть")

    class Meta:
        app_label = "settings"
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"

    def __str__(self):
        return str(self.social_network)


class UserFont(BaseFont):
    class Meta:
        app_label = "settings"
        verbose_name = "Бренд шрифт"
        verbose_name_plural = "Бренд шрифты"
        ordering = ["name"]


class Trackers(OneInstanceModel):
    common_metrics = models.CharField(max_length=10, verbose_name="Метрика: Общая")
    main_domain_metrics = models.CharField(max_length=10, verbose_name="Метрика: Банкомаг")
    partner_metrics = models.CharField(max_length=10, verbose_name="Метрика: Партнеры")
    profile_metrics = models.CharField(max_length=10, verbose_name="Метрика: Кабинет")
    
    class Meta:
        app_label = "settings"
        verbose_name = "Трекеры"
        verbose_name_plural = "Трекеры"