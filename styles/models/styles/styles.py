from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from blocks.models.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
    StagesBlock,
)
from blocks.models.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)

from styles.models.mixins.text_mixins import (
    ExplanationTextStylesMixin,
    SubheaderStylesMixin,
)
from styles.models.styles.base_custom_styles import BaseCustomStyles


def related_block(block_class):
    return models.OneToOneField(block_class, on_delete=models.CASCADE, related_name="styles")


class NavbarCustomStyles(BaseCustomStyles):
    block = related_block(Navbar)


class ContentCustomStyles(BaseCustomStyles):
    block = related_block(ContentBlock)
    border_radius = models.CharField(verbose_name="Радиус скругления картинки", null=True, blank=True, max_length=50)


class CoverCustomStyles(BaseCustomStyles):
    block = related_block(Cover)


class FeaturesCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin, SubheaderStylesMixin):
    block = related_block(FeaturesBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)
    icon_color = ColorField(verbose_name="Цвет иконок", default="#689F38")
    icon_background_color = ColorField(verbose_name="Цвет фона иконок", default="#FFFFFF")

    icon_width = models.CharField(verbose_name="Ширина иконок", max_length=20, null=True, blank=True)
    icon_height = models.CharField(verbose_name="Высота иконок", max_length=20, null=True, blank=True)


class RegisterCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(RegisterBlock)

    button_color = ColorField(verbose_name="цвет кнопки", null=True, blank=True)


class SocialCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(SocialMediaBlock)


class QuestionsCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(QuestionsBlock)


class StagesCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(StagesBlock)


class CatalogCustomStyles(BaseCustomStyles, SubheaderStylesMixin):
    block = related_block(CatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)


class MainPageCatalogCustomStyles(BaseCustomStyles, SubheaderStylesMixin):
    block = related_block(MainPageCatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)


class PromoCatalogCustomStyles(BaseCustomStyles):
    block = related_block(PromoCatalog)

    swiper_columns = models.PositiveIntegerField(verbose_name="Количество колонок в слайдере", default=3)


class AdditionalCatalogCustomStyles(BaseCustomStyles):
    block = related_block(AdditionalCatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)

    darkness_bottom = models.PositiveIntegerField(
        verbose_name="процент затемнения карточки снизу",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )
