import datetime
import random

from ckeditor.fields import RichTextField
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalog.models.products import Product
from common.security import LinkEncryptor


class Offer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

    annotation = models.TextField(max_length=300, verbose_name="Аннотация")
    description = RichTextField(max_length=5000, verbose_name="Описание")

    banner = models.ImageField(upload_to="products/banners/", verbose_name="Баннер", null=True, blank=True)
    promote = models.DateField(verbose_name="Продвигать до", null=True, blank=True)

    promotion = models.BooleanField(verbose_name="Акция")

    profit = models.CharField(max_length=500, verbose_name="Выгода", help_text="₽")

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
        verbose_name = "оффер"
        verbose_name_plural = "офферы"
        ordering = ["end_promotion"]

    def __str__(self):
        return self.name


class Link(models.Model):
    text = models.URLField(max_length=300, verbose_name="ссылка")
    percent = models.PositiveIntegerField(
        verbose_name="процент", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    info = models.CharField(verbose_name="Инфо", max_length=300, null=True, blank=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="links")

    class Meta:
        verbose_name = "ссылка"
        verbose_name = "ссылки"

    def __str__(self):
        return self.text
