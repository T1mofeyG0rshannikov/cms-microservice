from ckeditor.fields import RichTextField
from django.db import models

from .common import BaseBlock
from .mixins import ButtonMixin, TitleMixin

# from django.dispatch import receiver
# from blocks.models.common import Template
# from catalog.models.products import ProductType


class CatalogBlock(BaseBlock, TitleMixin, ButtonMixin):
    product_type = models.ForeignKey("catalog.ProductType", on_delete=models.CASCADE, null=True)
    introductory_text = RichTextField(verbose_name="Введение", max_length=300, null=True)
    add_exclusive = models.BooleanField(
        verbose_name="Эксклюзив", help_text="нужно ли добавлять карточку приватного продукта", null=True
    )

    class Meta:
        db_table = "blocks_catalogblock"
        verbose_name = "Блок каталога"
        verbose_name_plural = "Блоки каталога"


"""
@receiver(models.signals.post_save, sender=ProductType)
def execute_after_save(sender, instance, created, **kwargs):
    if created:
        try:
            catalog_template = Template.objects.get(file="catalog.html")
            CatalogBlock.objects.create(name=f"Каталог ({instance.name})", product_type=instance, template=catalog_template)
        except:
            pass
"""
