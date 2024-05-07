from django.db import models

from .blocks import FeaturesBlock
from .mixins import TitleMixin


class Feature(TitleMixin):
    icon = models.FileField(verbose_name="Иконка", upload_to="features")
    description = models.TextField(verbose_name="Пояснение")
    block = models.ForeignKey(
        FeaturesBlock, verbose_name="Блок", on_delete=models.SET_NULL, null=True, related_name="features"
    )

    def __str__(self):
        return self.title
