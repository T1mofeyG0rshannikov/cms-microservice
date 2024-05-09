from django.db import models


class TitleMixin(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
