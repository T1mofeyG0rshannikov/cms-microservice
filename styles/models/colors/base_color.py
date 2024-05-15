from django.db import models

from styles.models.mixins.color_mixins import ColorMixin


class BaseColor(ColorMixin):
    name = models.CharField(max_length=50)
