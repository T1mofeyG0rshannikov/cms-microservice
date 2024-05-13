from django.db import models


class SiteSettings(models.Model):
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return self._meta.verbose_name


class Logo(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="images/logo")
    width = models.CharField(verbose_name="Ширина", max_length=20)
    height = models.CharField(verbose_name="Высота", max_length=20)

    width_mobile = models.CharField(verbose_name="Ширина(смартфон)", max_length=20)
    height_mobile = models.CharField(verbose_name="Высота(смартфон)", max_length=20)

    settings = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name="logo")

    def __str__(self):
        return "Логотип"

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


class Icon(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="images/icon")

    settings = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name="icon")

    def __str__(self):
        return "Иконка"

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконка"
