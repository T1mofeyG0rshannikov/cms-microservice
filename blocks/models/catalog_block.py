from ckeditor.fields import RichTextField
from django.db import models

# from catalog.models.products import Product
# from catalog.serializers import CatalogProductSerializer
from blocks.models.blocks_components import CatalogProductType

from .common import BaseBlock
from .mixins import ButtonMixin, TitleMixin


class BaseCatalogBlock(BaseBlock, TitleMixin, ButtonMixin):
    introductory_text = RichTextField(verbose_name="Введение", max_length=300, null=True)
    add_exclusive = models.BooleanField(
        verbose_name="Эксклюзив", help_text="нужно ли добавлять карточку приватного продукта", null=True
    )
    # page_title = models.CharField(verbose_name="Заголовок страницы", max_length=100, null=True)

    class Meta:
        abstract = True


class CatalogBlock(BaseCatalogBlock):
    product_type = models.ForeignKey("catalog.ProductType", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "blocks_catalogblock"
        verbose_name = "Блок каталога"
        verbose_name_plural = "Блоки каталога"


class MainPageCatalogBlock(BaseCatalogBlock):
    page_title = models.CharField(verbose_name="Заголовок страницы", max_length=100, null=True)

    class Meta:
        verbose_name = "Блок каталога на главной"
        verbose_name_plural = "Блоки каталога на главной"

    # @property
    # def products(self):
    #    return [product.product for product in CatalogProductType.objects.filter(block=self)]

    # @products.setter
    # def products(self, serialized_products):
    #    self._products = serialized_products
