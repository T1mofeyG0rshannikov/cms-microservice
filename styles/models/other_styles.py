from django.db import models
from .common import BaseStyles


class MarginBlock(BaseStyles):
    margin_top = models.CharField(verbose_name=u"Отступ сверху", max_length=20)
    margin_bottom = models.CharField(verbose_name=u"Отступ снизу", max_length=20)
    
    class Meta:
        verbose_name = u"Отступы в блоке"
        verbose_name_plural = u"Отступы в блоке"

class IconSize(BaseStyles):
    height = models.CharField(verbose_name=u"Высота", max_length=20)
    width = models.CharField(verbose_name=u"Ширина", max_length=20)
    
    class Meta:
        verbose_name = u"Размер иконок"
        verbose_name_plural = u"Размер иконок"