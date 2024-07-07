from ckeditor.fields import RichTextField
from django.db import models

from catalog.models.products import Product

from .common import BaseBlock
from .mixins import ButtonMixin, TitleMixin


class BaseCatalogBlock(BaseBlock):
    class Meta:
        abstract = True


class CatalogBlock(BaseCatalogBlock, ButtonMixin, TitleMixin):
    introductory_text = RichTextField(verbose_name="Введение", max_length=1000, null=True)

    product_type = models.ForeignKey("catalog.ProductType", on_delete=models.CASCADE, null=True)

    add_exclusive = models.BooleanField(
        verbose_name="Эксклюзив", help_text="нужно ли добавлять карточку приватного продукта", null=True
    )

    class Meta:
        db_table = "blocks_catalogblock"
        verbose_name = "Блок каталога"
        verbose_name_plural = "Блоки каталога"


class MainPageCatalogBlock(BaseCatalogBlock, TitleMixin):
    introductory_text = RichTextField(verbose_name="Введение", max_length=1000, null=True)

    button_text = models.CharField(verbose_name="Текст кнопки", max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Блок каталога на главной"
        verbose_name_plural = "Блоки каталога на главной"


class AdditionalCatalogBlock(BaseCatalogBlock):
    button_text = models.CharField(verbose_name="Текст кнопки", max_length=20, null=True, blank=True)

    add_annotation = models.BooleanField(verbose_name="добавлять аннотацию к карточке", default=True)
    add_button = models.BooleanField(verbose_name="добавлять кнопку к карточке", default=True)

    class Meta:
        verbose_name = "Дополнительный каталог"
        verbose_name_plural = "Дополнительные каталоги"


class PromoCatalog(BaseBlock, TitleMixin):
    class Meta:
        verbose_name = "Промо акции"
        verbose_name_plural = "Промо акциий"

    @property
    def products(self):
        return Product.objects.all()
