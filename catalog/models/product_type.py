from ckeditor.fields import RichTextField
from django.db import models

from blocks.models.blocks import Cover
from offers.models import Offer


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория продуктов"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.name


class ProductType(models.Model):
    PRODUCT_TYPE_STATUSES = (("Опубликовано", "Опубликовано"), ("Скрыто", "Скрыто"))

    status = models.CharField(verbose_name="статус", choices=PRODUCT_TYPE_STATUSES, null=True, max_length=100)
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    image = models.ImageField(upload_to="organizations/covers", verbose_name="Этикетка", null=True)

    cover = models.ForeignKey(Cover, on_delete=models.SET_NULL, null=True, verbose_name="блок обложки")
    description = RichTextField(max_length=1000, verbose_name="Аннотация")

    profit = models.CharField(max_length=500, verbose_name="Выгода", null=True)

    class Meta:
        verbose_name = "Тип продукта/акции"
        verbose_name_plural = "Типы продукта/акции"

    def __str__(self):
        return self.name


class OfferTypeRelation(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.SET_NULL, null=True, verbose_name="Тип продукта", related_name="types"
    )
    type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True, verbose_name="продукт", related_name="products"
    )

    profit = models.CharField(max_length=500, verbose_name="Выгода")

    def __str__(self):
        return str(self.type)
