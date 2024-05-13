from django.db import models

from styles.models.styles.styles import GlobalStyles


class BaseStyles(models.Model):
    global_styles = models.OneToOneField(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self._meta.verbose_name
