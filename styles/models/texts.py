from .base_styles import BaseStyles
from .mixins.font_mixins import FontMixin
from .mixins.text_mixins import (
    InvertedTextColorMixin,
    SizeOfTextMixin,
    SizeOfTextMobileMixin,
    TextColorMinin,
    ThicknessOfTextMixin,
    ThicknessOfTextMobileMixin,
)


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
        verbose_name = "Текст пояснний"
        verbose_name_plural = "Текст пояснний"
