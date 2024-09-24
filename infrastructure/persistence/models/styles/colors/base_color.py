from django.db import models

from infrastructure.persistence.models.styles.mixins.color_mixins import ColorMixin


class BaseColor(ColorMixin):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "styles"
