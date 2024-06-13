from django.db import models


class Site(models.Model):
    domen = models.CharField(max_length=50, verbose_name="домен")
    logo = models.ImageField(verbose_name="Лого", upload_to="images/logo")
    logo_width = models.CharField(verbose_name="ширина лого", max_length=20, null=True)
    logo_width_mobile = models.CharField(verbose_name="ширина лого(мобильный)", max_length=20, null=True)
    logo2 = models.ImageField(verbose_name="Лого для форм", upload_to="images/logo")
    is_active = models.BooleanField(verbose_name="активный", default=True)
    use_default_settings = models.BooleanField(verbose_name="Использовать общие настройки сайта", default=False)
    advertising_channel = models.CharField(verbose_name="Рекламный канал", null=True, max_length=100)

    class Meta:
        verbose_name = "сайт"
        verbose_name_plural = "сайты"

    def __str__(self):
        return self.domen
