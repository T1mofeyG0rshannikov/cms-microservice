from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from infrastructure.persistence.models.blocks.common import BasePageBlock, BasePageModel


class CatalogPageTemplate(BasePageModel):
    title = models.CharField(verbose_name="Заголовок", max_length=50)

    class Meta:
        app_label = "catalog"
        verbose_name = "каталог"
        verbose_name_plural = "каталог"

    def __str__(self):
        return self.title


class Block(BasePageBlock):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="catalog_content_type", null=True
    )
    block_id = models.PositiveIntegerField(null=True)
    block = GenericForeignKey("content_type", "block_id")
    page = models.ForeignKey(
        CatalogPageTemplate, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE
    )

    class Meta(BasePageBlock.Meta):
        app_label = "catalog"
