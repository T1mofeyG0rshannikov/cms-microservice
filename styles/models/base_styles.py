from django.db import models

from .common import GlobalStyles


class BaseStyles(models.Model):
    global_styles = models.ForeignKey(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self._meta.verbose_name
