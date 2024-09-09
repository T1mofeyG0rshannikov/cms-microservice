from ckeditor.fields import RichTextField
from django.db import models

from blocks.models.mixins import ButtonMixin
from common.models import OneInstanceModel


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

    admin_hint = RichTextField(max_length=1500, verbose_name="пояснение", null=True, blank=True)
    partner_program = models.CharField(max_length=100, null=True, blank=True, verbose_name="Партнерская программа")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class Product(models.Model):
    organization = models.ForeignKey(
        Organization, related_name="products", on_delete=models.CASCADE, verbose_name="организация"
    )
    cover = models.ImageField(upload_to="products/covers", verbose_name="Обложка")

    name = models.CharField(max_length=100, verbose_name="Название")

    category = models.ForeignKey(
        "catalog.ProductCategory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name="категория",
    )

    PRODUCT_STATUS = (("Черновик", "Черновик"), ("Архив", "Архив"), ("Опубликовано", "Опубликовано"))

    status = models.CharField(verbose_name="статус", choices=PRODUCT_STATUS, max_length=50, default="Новое")

    private = models.BooleanField(verbose_name="Приватный(виден только зарегистрированным пользователям)")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    partner_annotation = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Партнерская аннотация")
    partner_bonus = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Партнерский бонус")
    partner_description = RichTextField(max_length=5000, null=True, blank=True, verbose_name="Партнерское описание")

    class Meta:
        verbose_name = "продукт/акция"
        verbose_name_plural = "продукты/акции"

    def __str__(self):
        return self.name


class ExclusiveCard(OneInstanceModel, ButtonMixin):
    image = models.ImageField(verbose_name="картинка", upload_to="images/exclusive")
    bonus = models.CharField(verbose_name="бонус", max_length=50)

    annotation = models.TextField(verbose_name="аннотация", max_length=700, null=True)

    class Meta:
        verbose_name = "Карточка Эксклюзив"
        verbose_name_plural = "Карточка Эксклюзив"
