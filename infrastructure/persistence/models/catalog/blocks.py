from django.db import models

from web.common.models import BasePageBlock, BlockRelationship


class CatalogPageTemplate(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=50)

    class Meta:
        app_label = "catalog"
        verbose_name = "каталог"
        verbose_name_plural = "каталог"

    def __str__(self):
        return self.title


class Block(BasePageBlock):
    name = models.ForeignKey(
        BlockRelationship, verbose_name="Блок", on_delete=models.CASCADE, related_name="catalog_block"
    )
    page = models.ForeignKey(
        CatalogPageTemplate, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE
    )

    class Meta(BasePageBlock.Meta):
        app_label = "catalog"
