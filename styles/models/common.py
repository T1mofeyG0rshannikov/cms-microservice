from django.db import models


class GlobalStyles(models.Model):
    class Meta:
        verbose_name = "Глобальные стили"
        verbose_name_plural = "Глобальные стили"

    def __str__(self):
        return self._meta.verbose_name


class BaseStyles(models.Model):
    global_styles = models.ForeignKey(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self._meta.verbose_name


class Font(models.Model):
    name = models.CharField(verbose_name="Имя шрифта", max_length=50)
    link = models.CharField(verbose_name="Ссылка для подключения", max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Шрифт"
        verbose_name_plural = "Шрифты"

    def __str__(self):
        return self.name
