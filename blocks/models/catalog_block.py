from ckeditor.fields import RichTextField
from django.db import models

from catalog.models.products import ProductType

from .common import BaseBlock
from .mixins import ButtonMixin, TitleMixin


class CatalogBlock(BaseBlock, TitleMixin, ButtonMixin):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    introductory_text = RichTextField(verbose_name="Введение", max_length=300)
    add_exclusive = models.BooleanField(
        verbose_name="Эксклюзив", help_text="нужно ли добавлять карточку приватного продукта"
    )

    class Meta:
        db_table = "blocks_catalogblock"
        verbose_name = "Блок каталога"
        verbose_name_plural = "Блоки каталога"
