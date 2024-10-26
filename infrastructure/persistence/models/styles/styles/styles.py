from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from infrastructure.persistence.models.blocks.blocks import (
    ContentBlock,
    Cover,
    FeaturesBlock,
    Footer,
    Navbar,
    QuestionsBlock,
    RegisterBlock,
    SocialMediaBlock,
    StagesBlock,
)
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.models.styles.mixins.text_mixins import (
    ExplanationTextStylesMixin,
    SubheaderStylesMixin,
)
from infrastructure.persistence.models.styles.styles.base_custom_styles import (
    BaseCustomStyles,
)


def related_block(block_class):
    return models.OneToOneField(block_class, on_delete=models.CASCADE, related_name="styles")


class NavbarCustomStyles(BaseCustomStyles):
    block = related_block(Navbar)

    class Meta:
        app_label = "styles"


class ContentCustomStyles(BaseCustomStyles):
    block = related_block(ContentBlock)
    border_radius = models.CharField(verbose_name="Радиус скругления картинки", null=True, blank=True, max_length=50)

    class Meta:
        app_label = "styles"


class CoverCustomStyles(BaseCustomStyles):
    block = related_block(Cover)

    class Meta:
        app_label = "styles"


class FooterCustomStyles(BaseCustomStyles):
    block = related_block(Footer)

    class Meta:
        app_label = "styles"


class FeaturesCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin, SubheaderStylesMixin):
    block = related_block(FeaturesBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)
    icon_color = ColorField(verbose_name="Цвет иконок", default="#689F38")
    icon_background_color = ColorField(verbose_name="Цвет фона иконок", default="#FFFFFF")

    icon_width = models.CharField(verbose_name="Ширина иконок", max_length=20, null=True, blank=True)
    icon_height = models.CharField(verbose_name="Высота иконок", max_length=20, null=True, blank=True)

    class Meta:
        app_label = "styles"


class RegisterCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(RegisterBlock)

    button_color = ColorField(verbose_name="цвет кнопки", null=True, blank=True)

    class Meta:
        app_label = "styles"


class SocialCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(SocialMediaBlock)

    class Meta:
        app_label = "styles"


class QuestionsCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(QuestionsBlock)

    class Meta:
        app_label = "styles"


class StagesCustomStyles(BaseCustomStyles, ExplanationTextStylesMixin):
    block = related_block(StagesBlock)

    class Meta:
        app_label = "styles"


class CatalogCustomStyles(BaseCustomStyles, SubheaderStylesMixin):
    block = related_block(CatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)

    class Meta:
        app_label = "styles"


class MainPageCatalogCustomStyles(BaseCustomStyles, SubheaderStylesMixin):
    block = related_block(MainPageCatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)

    class Meta:
        app_label = "styles"


class PromoCatalogCustomStyles(BaseCustomStyles):
    block = related_block(PromoCatalog)

    swiper_columns = models.PositiveIntegerField(verbose_name="Количество колонок в слайдере", default=3)

    class Meta:
        app_label = "styles"


class AdditionalCatalogCustomStyles(BaseCustomStyles):
    block = related_block(AdditionalCatalogBlock)

    columns = models.PositiveIntegerField(verbose_name="Количество колонок", default=4)

    darkness_bottom = models.PositiveIntegerField(
        verbose_name="процент затемнения карточки снизу",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "styles"
