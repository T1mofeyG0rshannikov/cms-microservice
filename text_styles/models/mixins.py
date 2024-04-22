from colorfield.fields import ColorField
from django.db import models


class ColorMixin(models.Model):
    color = ColorField(verbose_name=u"Цвет", default='#FFFFFF')
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self._meta.verbose_name

class FontMixin(models.Model):
    font = models.CharField(verbose_name=u"Шрифт для текста", max_length=15)
    
    class Meta:
        abstract = True
        
class ThicknessOfTextMixin(models.Model):
    fontWeight = models.CharField(verbose_name=u"Толщина текста", max_length=15)
    
    class Meta:
        abstract = True
        
class ThicknessOfTextMobileMixin(models.Model):
    fontWeightMobile = models.CharField(verbose_name=u"Толщина текста(мобильный)", max_length=15)
    
    class Meta:
        abstract = True
        
class SizeOfTextMixin(models.Model):
    fontSize = models.CharField(verbose_name=u"Размер текста", max_length=15)
    
    class Meta:
        abstract = True

class SizeOfTextMobileMixin(models.Model):
    fontSizeMobile = models.CharField(verbose_name=u"Размер текста(мобильный)", max_length=15)
    
    class Meta:
        abstract = True

class TextColorMinin(ColorMixin):
    class Meta:
        verbose_name = u"Цвет текста"
        abstract = True

class InvertedTextColorMixin(ColorMixin):
    fontColorInverted = ColorField(verbose_name=u"Инвертированный цвет текста")
    
    class Meta:
        verbose_name = u"Инвертированный цвет текста"
        abstract = True