from django.db import models

from .blocks import FeaturesBlock, Navbar
from .mixins import ButtonMixin, TitleMixin


class NavMenuItem(ButtonMixin):
    navbar = models.ForeignKey(Navbar, on_delete=models.SET_NULL, null=True, related_name="menu_items")


class Feature(TitleMixin):
    icon = models.ImageField(verbose_name="Иконка", upload_to="features")
    description = models.TextField(verbose_name="Пояснение")
    block = models.ForeignKey(
        FeaturesBlock, verbose_name="Блок", on_delete=models.SET_NULL, null=True, related_name="features"
    )

    def __str__(self):
        return self.description
