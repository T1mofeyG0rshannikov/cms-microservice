from django.db import models

from infrastructure.persistence.models.common import BasePageBlock, BlockRelationship
from infrastructure.persistence.models.settings import LandingDomain


class Landing(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=50)
    url = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(verbose_name="Лого", upload_to="images/logo", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Название")
    domain = models.ForeignKey(LandingDomain, on_delete=models.SET_NULL, null=True)

    class Meta:
        app_label = "blocks"


class LandingBlock(BasePageBlock):
    name = models.ForeignKey(
        BlockRelationship, verbose_name="Блок", on_delete=models.CASCADE, related_name="landing_block"
    )
    page = models.ForeignKey(Landing, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE)

    class Meta(BasePageBlock.Meta):
        app_label = "blocks"
