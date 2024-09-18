import datetime
import random

from ckeditor.fields import RichTextField
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from infrastructure.security import LinkEncryptor
from web.blocks.models.mixins import ButtonMixin
from web.catalog.models.product_type import ProductCategory, ProductType
from web.common.models import OneInstanceModel


class OrganizationType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        app_label = "catalog"
        db_table = "catalog_organizationtype"
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
        ProductCategory,
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
        return f"{self.organization}: {self.name} ({self.category})"


class ExclusiveCard(OneInstanceModel, ButtonMixin):
    image = models.ImageField(verbose_name="картинка", upload_to="images/exclusive")
    bonus = models.CharField(verbose_name="бонус", max_length=50)

    annotation = models.TextField(verbose_name="аннотация", max_length=700, null=True)

    class Meta:
        verbose_name = "Карточка Эксклюзив"
        verbose_name_plural = "Карточка Эксклюзив"


class Offer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="offers")

    annotation = models.TextField(max_length=300, verbose_name="Аннотация")
    description = RichTextField(max_length=5000, verbose_name="Описание")

    banner = models.ImageField(upload_to="products/banners/", verbose_name="Баннер", null=True, blank=True)
    promote = models.DateField(verbose_name="Продвигать до", null=True, blank=True)

    promotion = models.BooleanField(verbose_name="Акция")

    start_promotion = models.DateField(verbose_name="Начало акции", null=True, blank=True)
    end_promotion = models.DateField(verbose_name="Окончание акции", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    PRODUCT_STATUS = (("Черновик", "Черновик"), ("Архив", "Архив"), ("Опубликовано", "Опубликовано"))

    status = models.CharField(verbose_name="статус", choices=PRODUCT_STATUS, max_length=50, default="Новое")

    terms_of_the_promotion = models.URLField(max_length=1000, null=True, blank=True, verbose_name="условия акции")

    partner_programs = (
        ("Приведи друга", "Приведи друга"),
        ("CPA сеть", "CPA сеть"),
        ("Друзья/CPA", "Друзья/CPA"),
        ("Только админ", "Только админ"),
        ("Нет", "Нет"),
    )

    partner_program = models.CharField(
        max_length=100, choices=partner_programs, null=True, verbose_name="Партнерская программа"
    )
    verification_of_registration = models.BooleanField(default=False, verbose_name="Верификация оформления")

    link_encryptor = LinkEncryptor()

    @property
    def get_end_promotion(self):
        date = self.end_promotion
        if date is None:
            date = datetime.date.today() + relativedelta(years=+1)

        return date

    @property
    def link(self):
        links = self.links.all()

        link_change = []

        for i in range(len(links)):
            for j in range(links[i].percent):
                link_change.append(i)

        if link_change:
            link = links[random.choice(link_change)].text
            link = self.link_encryptor.encrypt(link)

            return link

        return ""

    class Meta:
        db_table = "offers_offer"
        verbose_name = "оффер"
        verbose_name_plural = "офферы"
        ordering = ["end_promotion"]

    def __str__(self):
        return f"{self.product.organization}: {self.name} ({self.product.category})"


class Link(models.Model):
    text = models.URLField(max_length=300, verbose_name="ссылка")
    percent = models.PositiveIntegerField(
        verbose_name="процент", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    info = models.CharField(verbose_name="Инфо", max_length=300, null=True, blank=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="links")

    class Meta:
        db_table = "offers_link"
        verbose_name = "ссылка"
        verbose_name = "ссылки"

    def __str__(self):
        return self.text


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
