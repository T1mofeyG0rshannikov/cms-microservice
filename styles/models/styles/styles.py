from colorfield.fields import ColorField
from django.db import models

from blocks.models.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
)
from styles.models.mixins.text_mixins import ExplanationTextStylesMixin

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
    block = models.OneToOneField(ContentBlock, on_delete=models.SET_NULL, null=True)
    border_radius = models.CharField(verbose_name="Радиус скругления картинки", null=True, blank=True, max_length=50)


class CoverCustomStyles(BaseCustomStyles):
    block = models.OneToOneField(Cover, on_delete=models.SET_NULL, null=True)


class FeaturesCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = models.OneToOneField(FeaturesBlock, on_delete=models.SET_NULL, null=True)
    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)
    icon_color = ColorField(verbose_name="Цвет иконок", default="#689F38")
    icon_background_color = ColorField(verbose_name="Цвет фона иконок", default="#FFFFFF")

    icon_width = models.CharField(verbose_name="Ширина иконок", max_length=20, null=True, blank=True)
    icon_height = models.CharField(verbose_name="Высота иконок", max_length=20, null=True, blank=True)

    subheader_size = models.CharField(verbose_name="размер подзаголовка", max_length=50, null=True, blank=True)
    subheader_size_mobile = models.CharField(
        verbose_name="размер подзаголовка (смартфон)", max_length=50, null=True, blank=True
    )
    subheader_thickness = models.CharField(verbose_name="толщина подзаголовка", max_length=50, null=True, blank=True)
    subheader_thickness_mobile = models.CharField(
        verbose_name="толщина подзаголовка (смартфон)", max_length=50, null=True, blank=True
    )
    subheader_color = ColorField(verbose_name="Цвет подзаголовка", null=True, blank=True)


class RegisterCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = models.OneToOneField(RegisterBlock, on_delete=models.SET_NULL, null=True)

    button_color = ColorField(verbose_name="цвет кнопки", null=True, blank=True)


class SocialCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = models.OneToOneField(SocialMediaBlock, on_delete=models.SET_NULL, null=True)


class QuestionsCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = models.OneToOneField(QuestionsBlock, on_delete=models.SET_NULL, null=True)
