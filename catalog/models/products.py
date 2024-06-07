from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalog.models.product_type import ProductType


class OrganizationType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Тип организации"
        verbose_name_plural = "Типы организаций"

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE, verbose_name="Тип")

    logo = models.ImageField(upload_to="organizations/logos/", verbose_name="Лого")
    site = models.URLField(verbose_name="сайт", max_length=500)

    admin_hint = models.CharField(max_length=100, verbose_name="пояснение для админа")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="организация")
    cover = models.ImageField(upload_to="products/covers", verbose_name="Обложка")

    name = models.CharField(max_length=100, verbose_name="Название продукта")
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name="Тип продукта")
    annotation = models.CharField(max_length=300, verbose_name="Аннотация")
    description = RichTextField(max_length=5000, verbose_name="Описание")

    banner = models.ImageField(upload_to="products/banners/", verbose_name="Баннер", null=True, blank=True)
    promote = models.DateField(verbose_name="Продвигать до", null=True, blank=True)

    private = models.BooleanField(verbose_name="Приватный(виден только зарегистрированным пользователям)")
    promotion = models.BooleanField(verbose_name="Акция")

    profit = models.CharField(max_length=500, verbose_name="Выгода")

    start_promotion = models.DateField(verbose_name="Начало акции", null=True, blank=True)
    end_promotion = models.DateField(verbose_name="Окончание акции", null=True, blank=True)

    class Meta:
        verbose_name = "продукт/акция"
        verbose_name_plural = "продукты/акции"

    def __str__(self):
        return self.name


class Link(models.Model):
    text = models.URLField(max_length=300, verbose_name="ссылка")
    percent = models.PositiveIntegerField(
        verbose_name="процент", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="links")

    class Meta:
        verbose_name = "ссылка"
        verbose_name = "ссылки"

    def __str__(self):
        return self.text
