from django.db import models

from blocks.models.blocks import Cover


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    image = models.ImageField(upload_to="organizations/covers", verbose_name="Картинка блока типа продукта", null=True)

    cover = models.ForeignKey(Cover, on_delete=models.SET_NULL, null=True, verbose_name="блок обложки")
    description = models.CharField(max_length=500, verbose_name="Описание")

    profit = models.CharField(max_length=500, verbose_name="Выгода")

    class Meta:
        verbose_name = "Тип продукта/акции"
        verbose_name_plural = "Типы продукта/акции"

    def __str__(self):
        return self.name
