from django.db import models

from blocks.models.blocks import Cover, ExampleBlock, Navbar

from .abstract_classes import BaseCustomStyles


class GlobalStyles(models.Model):
    class Meta:
        verbose_name = "Глобальные стили"
        verbose_name_plural = "Глобальные стили"

    def __str__(self):
        return self._meta.verbose_name


class NavbarCustomStyles(BaseCustomStyles):
    block = models.ForeignKey(Navbar, on_delete=models.SET_NULL, null=True)


class ContentCustomStyles(BaseCustomStyles):
    block = models.ForeignKey(ExampleBlock, on_delete=models.SET_NULL, null=True)


class CoverCustomStyles(BaseCustomStyles):
    block = models.ForeignKey(Cover, on_delete=models.SET_NULL, null=True)
