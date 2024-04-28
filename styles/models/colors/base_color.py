from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from ..mixins.color_mixins import ColorMixin


class BaseColor(ColorMixin):
    name = models.CharField(max_length=50)

    # def __str__(self):
    #    print(self.color)
    #    print(f"<div style='background-color: {self.color}; width: 50px; height: 30px;'>{self.color}</div>")
    #    return format_html(f"<div style='background-color: {self.color}; width: 50px; height: 30px;'>{self.color}</div>")
    #    return mark_safe(f"<div style='background-color: {self.color}; width: 50px; height: 30px;'>{self.color}</div>")
