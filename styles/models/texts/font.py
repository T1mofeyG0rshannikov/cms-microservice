from django.db import models


class Font(models.Model):
    name = models.CharField(verbose_name="Имя шрифта", max_length=50)
    link = models.CharField(verbose_name="Ссылка для подключения", max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Шрифт"
        verbose_name_plural = "Шрифты"

    def __str__(self):
        return self.name
