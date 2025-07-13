from ckeditor.fields import RichTextField
from django.db import models

from infrastructure.persistence.models.blocks.common import BaseBlock
from infrastructure.persistence.models.blocks.mixins import ButtonMixin, TitleMixin
from infrastructure.persistence.models.catalog.product_type import ProductType


class CatalogBlock(BaseBlock, ButtonMixin, TitleMixin):
    introductory_text = RichTextField(verbose_name="Введение", max_length=1000, null=True)

    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)

    add_exclusive = models.BooleanField(
        verbose_name="Эксклюзив", help_text="нужно ли добавлять карточку приватного продукта", null=True
    )

    add_category = models.BooleanField(verbose_name="Показывать категорию", null=True)

    class Meta:
        app_label = "blocks"
        verbose_name = "каталог"
        verbose_name_plural = "каталог"


class MainPageCatalogBlock(BaseBlock, TitleMixin):
    introductory_text = RichTextField(verbose_name="Введение", max_length=1000, null=True)

    button_text = models.CharField(verbose_name="Текст кнопки", max_length=20, null=True, blank=True)

    class Meta:
        app_label = "blocks"
        verbose_name = "Витрина"
        verbose_name_plural = "Витрина"


class AdditionalCatalogBlock(BaseBlock):
    button_text = models.CharField(verbose_name="Текст кнопки", max_length=20, null=True, blank=True)

    add_annotation = models.BooleanField(verbose_name="добавлять аннотацию к карточке", default=True)
    add_button = models.BooleanField(verbose_name="добавлять кнопку к карточке", default=True)

    class Meta:
        app_label = "blocks"
        verbose_name = "Мини витрина"
        verbose_name_plural = "Мини витрины"


class PromoCatalog(BaseBlock, TitleMixin):
    class Meta:
        app_label = "blocks"
        verbose_name = "Промо"
        verbose_name_plural = "Промо"
