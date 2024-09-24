from django.db import models

from infrastructure.persistence.models.styles.mixins.color_mixins import MarginMixin
from infrastructure.persistence.models.styles.styles.base_styles import BaseStyles


class MarginBlock(MarginMixin, BaseStyles):
    class Meta:
        app_label = "styles"
        verbose_name = "Отступы в блоке"
        verbose_name_plural = "Отступы в блоке"


class IconSize(BaseStyles):
    height = models.CharField(verbose_name="Высота", max_length=20)
    width = models.CharField(verbose_name="Ширина", max_length=20)

    class Meta:
        app_label = "styles"
        verbose_name = "Размер иконок"
        verbose_name_plural = "Размер иконок"
