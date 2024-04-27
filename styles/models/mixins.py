from colorfield.fields import ColorField
from django.db import models

from .common import Font


class ColorMixin(models.Model):
    color = ColorField(verbose_name="Цвет", default="#FFFFFF")

    class Meta:
        abstract = True

    def __str__(self):
        return self._meta.verbose_name


class FontMixin(models.Model):
    font = models.ForeignKey(Font, verbose_name="Шрифт для текста", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ThicknessOfTextMixin(models.Model):
    fontWeight = models.CharField(verbose_name="Толщина текста", max_length=15)

    class Meta:
        abstract = True


class ThicknessOfTextMobileMixin(models.Model):
    fontWeightMobile = models.CharField(verbose_name="Толщина текста(мобильный)", max_length=15)

    class Meta:
        abstract = True


class SizeOfTextMixin(models.Model):
    fontSize = models.CharField(verbose_name="Размер текста", max_length=15)

    class Meta:
        abstract = True


class SizeOfTextMobileMixin(models.Model):
    fontSizeMobile = models.CharField(verbose_name="Размер текста(мобильный)", max_length=15)

    class Meta:
        abstract = True


class TextColorMinin(ColorMixin):
    class Meta:
        verbose_name = "Цвет текста"
        abstract = True


class InvertedTextColorMixin(ColorMixin):
    fontColorInverted = ColorField(verbose_name="Инвертированный цвет текста")

    class Meta:
        verbose_name = "Инвертированный цвет текста"
        abstract = True
