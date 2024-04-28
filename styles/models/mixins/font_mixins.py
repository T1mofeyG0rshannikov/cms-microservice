from django.db import models

from styles.models.texts.font import Font


class FontMixin(models.Model):
    font = models.ForeignKey(Font, verbose_name="Шрифт для текста", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
