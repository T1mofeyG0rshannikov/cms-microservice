from .common import BaseStyles
from colorfield.fields import ColorField


class ColorStyles(BaseStyles):
    main_color = ColorField(verbose_name=u"Основной цвет", default='#FFFFFF')
    secondary_color = ColorField(verbose_name=u"Вторичный цвет", default='#FFFFFF')
    background_color = ColorField(verbose_name=u"Цвет фона", default='#FFFFFF')
    second_background_color = ColorField(verbose_name=u"Цвет фона 2", default='#FFFFFF')
    
    class Meta:
        verbose_name = u"Цвета"
        verbose_name_plural = u"Цвета"
