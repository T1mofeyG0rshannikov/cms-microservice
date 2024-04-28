from django.db import models


class MarginMixin(models.Model):
    margin_top = models.CharField(verbose_name="Отступ сверху", max_length=20, null=True, blank=True)
    margin_bottom = models.CharField(verbose_name="Отступ снизу", max_length=20, null=True, blank=True)

    class Meta:
        abstract = True
