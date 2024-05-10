from django.db import models


class TitleMixin(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class ButtonMixin(models.Model):
    button_text = models.CharField(verbose_name="Текст кнопки", max_length=20, null=True, blank=True)
    button_ref = models.CharField(verbose_name="Ссылка для кнопки", max_length=20, null=True, blank=True)

    class Meta:
        abstract = True
