from colorfield.fields import ColorField
from django.db import models


class ColorMixin(models.Model):
    color = ColorField(verbose_name=u"Цвет", default='#FFFFFF')
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self._meta.verbose_name