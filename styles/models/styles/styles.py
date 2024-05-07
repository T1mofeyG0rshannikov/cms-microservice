from django.db import models

from blocks.models.blocks import Cover, ExampleBlock, FeaturesBlock, Navbar

from .base_custom_styles import BaseCustomStyles


class GlobalStyles(models.Model):
    class Meta:
        verbose_name = "Глобальные стили"
        verbose_name_plural = "Глобальные стили"

    def __str__(self):
        return self._meta.verbose_name


class NavbarCustomStyles(BaseCustomStyles):
    block = models.OneToOneField(Navbar, on_delete=models.SET_NULL, null=True)


class ContentCustomStyles(BaseCustomStyles):
    block = models.OneToOneField(ExampleBlock, on_delete=models.SET_NULL, null=True)


class CoverCustomStyles(BaseCustomStyles):
    block = models.OneToOneField(Cover, on_delete=models.SET_NULL, null=True)


class FeaturesCustomStyles(BaseCustomStyles):
    block = models.OneToOneField(FeaturesBlock, on_delete=models.SET_NULL, null=True)
    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)
