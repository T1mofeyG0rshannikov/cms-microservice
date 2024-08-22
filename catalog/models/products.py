import random

from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from blocks.models.mixins import ButtonMixin
from catalog.models.product_type import ProductType
from common.models import OneInstanceModel
from common.security import LinkEncryptor


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

    admin_hint = RichTextField(max_length=1500, verbose_name="пояснение для админа")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


PRODUCT_STATUS = (("Черновик", "Черновик"), ("Архив", "Архив"), ("Опубликовано", "Опубликовано"))


class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="организация")
    cover = models.ImageField(upload_to="products/covers", verbose_name="Обложка")

    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name="Тип продукта")
    annotation = models.CharField(max_length=300, verbose_name="Аннотация")
    description = RichTextField(max_length=5000, verbose_name="Описание")

    banner = models.ImageField(upload_to="products/banners/", verbose_name="Баннер", null=True, blank=True)
    promote = models.DateField(verbose_name="Продвигать до", null=True, blank=True)

    private = models.BooleanField(verbose_name="Приватный(виден только зарегистрированным пользователям)")
    promotion = models.BooleanField(verbose_name="Акция")

    profit = models.CharField(max_length=500, verbose_name="Выгода", help_text="₽")

    start_promotion = models.DateField(verbose_name="Начало акции", null=True, blank=True)
    end_promotion = models.DateField(verbose_name="Окончание акции", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    status = models.CharField(verbose_name="статус", choices=PRODUCT_STATUS, max_length=50, default="Новое")

    terms_of_the_promotion = models.URLField(max_length=1000, null=True, blank=True, verbose_name="условия акции")
    partner_annotation = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Партнерская аннотация")
    partner_bonus = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Партнерский бонус")
    partner_description = RichTextField(max_length=5000, null=True, blank=True, verbose_name="Партнерское описание")

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
        verbose_name = "продукт/акция"
        verbose_name_plural = "продукты/акции"
        ordering = ["end_promotion"]

    def __str__(self):
        return self.name


class Link(models.Model):
    text = models.URLField(max_length=300, verbose_name="ссылка")
    percent = models.PositiveIntegerField(
        verbose_name="процент", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    info = models.CharField(verbose_name="Инфо", max_length=300, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="links")

    class Meta:
        verbose_name = "ссылка"
        verbose_name = "ссылки"

    def __str__(self):
        return self.text


class ExclusiveCard(OneInstanceModel, ButtonMixin):
    image = models.ImageField(verbose_name="картинка", upload_to="images/exclusive")
    bonus = models.CharField(verbose_name="бонус", max_length=50)

    annotation = models.TextField(verbose_name="аннотация", max_length=700, null=True)

    class Meta:
        verbose_name = "Карточка Эксклюзив"
        verbose_name_plural = "Карточка Эксклюзив"
