from .mixins import ColorMixin


class MainColor(ColorMixin):
    class Meta:
        verbose_name = u"Основной цвет"
        verbose_name_plural = u"Основной цвет"

class SecondaryColor(ColorMixin):
    class Meta:
        verbose_name = u"Вторичный цвет"
        verbose_name_plural = u"Вторичный цвет"

class BackgroundColor(ColorMixin):
    class Meta:
        verbose_name = u"Цвет фона"
        verbose_name_plural = u"Цвет фона"

class BackgroundColorSecond(ColorMixin):
    class Meta:
        verbose_name = u"Цвет фона 2"
        verbose_name_plural = u"Цвет фона 2"