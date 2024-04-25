from django.db import models


class GlobalStyles(models.Model):
    class Meta:
        verbose_name = u"Глобальные стили"
        verbose_name_plural = u"Глобальные стили"
        
    def __str__(self):
        return self._meta.verbose_name

class BaseStyles(models.Model):
    global_styles = models.ForeignKey(GlobalStyles, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self._meta.verbose_name