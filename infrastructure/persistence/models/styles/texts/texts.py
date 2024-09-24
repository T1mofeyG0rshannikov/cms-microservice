from infrastructure.persistence.models.styles.mixins.font_mixins import FontMixin
from infrastructure.persistence.models.styles.mixins.text_mixins import (
    InvertedTextColorMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    TextColorMinin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
)
from infrastructure.persistence.models.styles.styles.base_styles import BaseStyles


class HeaderText(
    BaseStyles,
    FontMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
    TextColorMinin,
    InvertedTextColorMixin,
):
    class Meta:
        app_label = "styles"
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовок"


class SubheaderText(
    BaseStyles,
    FontMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
    TextColorMinin,
    InvertedTextColorMixin,
):
    class Meta:
        app_label = "styles"
        verbose_name = "Подзаголовок"
        verbose_name_plural = "Подзаголовок"


class MainText(
    BaseStyles,
    FontMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
    TextColorMinin,
    InvertedTextColorMixin,
):
    class Meta:
        app_label = "styles"
        verbose_name = "Основной текст"
        verbose_name_plural = "Основной текст"


class ExplanationText(
    BaseStyles,
    FontMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
    TextColorMinin,
    InvertedTextColorMixin,
):
    class Meta:
        app_label = "styles"
        verbose_name = "Текст пояснний"
        verbose_name_plural = "Текст пояснний"
