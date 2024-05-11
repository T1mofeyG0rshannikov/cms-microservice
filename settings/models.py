from django.db import models


class Logo(models.Model):
    image = models.ImageField(verbose_name=u"Изображение", upload_to="images/logo")
    width = models.CharField(verbose_name=u"Ширина", max_length=20)
    height = models.CharField(verbose_name=u"Высота", max_length=20)

    width_mobile = models.CharField(verbose_name=u"Ширина(смартфон)", max_length=20)
    height_mobile = models.CharField(verbose_name=u"Высота(смартфон)", max_length=20)

    def __str__(self):
        return u"Логотип"

    class Meta:
        verbose_name = u"Логотип"
        verbose_name_plural = u"Логотип"
        
class Icon(models.Model):
    image = models.ImageField(verbose_name=u"Изображение", upload_to="images/icon")
    
    def __str__(self):
        return u"Иконка"

    class Meta:
        verbose_name = u"Иконка"
        verbose_name_plural = u"Иконка"