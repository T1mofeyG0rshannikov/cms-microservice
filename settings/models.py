from django.db import models

from common.models import OneInstanceModel


class SiteSettings(OneInstanceModel):
    disable_partners_sites = models.BooleanField(default=False, verbose_name="Отключить партнёрский домен")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"


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
        verbose_name = "Иконка"
        verbose_name_plural = "Иконка"
