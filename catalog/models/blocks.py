from django.db import models

from common.models import BasePageBlock, BlockRelationship


class CatalogPageTemplate(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=50)

    class Meta:
        verbose_name = "Шаблон страницы каталога"
        verbose_name_plural = "Шаблон страницы каталога"

    def __str__(self):
        return self.title


class Block(BasePageBlock):
    name = models.ForeignKey(
        BlockRelationship, verbose_name="Блок", on_delete=models.CASCADE, related_name="catalog_block"
    )
    page = models.ForeignKey(
        CatalogPageTemplate, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE
    )
