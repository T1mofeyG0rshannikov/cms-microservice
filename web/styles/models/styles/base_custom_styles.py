from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from styles.models.mixins.margin_mixin import MarginMixin


class BaseCustomStyles(MarginMixin):
    background_color = ColorField(verbose_name="Цвет фона", null=True, blank=True)
    photo_darkness = models.PositiveIntegerField(
        verbose_name="Затемнение фото в процентах",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    header_size = models.CharField(verbose_name="размер заголовка", max_length=50, null=True, blank=True)
    header_size_mobile = models.CharField(
        verbose_name="размер заголовка (смартфон)", max_length=50, null=True, blank=True
    )
    header_thickness = models.CharField(verbose_name="толщина заголовка", max_length=50, null=True, blank=True)
    header_thickness_mobile = models.CharField(
        verbose_name="толщина заголовка (смартфон)", max_length=50, null=True, blank=True
    )
    header_color = ColorField(verbose_name="Цвет заголовка", null=True, blank=True)

    main_text_size = models.CharField(verbose_name="размер основного текста", max_length=50, null=True, blank=True)
    main_text_size_mobile = models.CharField(
        verbose_name="размер основного текста (смартфон)", max_length=50, null=True, blank=True
    )
    main_text_thickness = models.CharField(
        verbose_name="толщина основного текста", max_length=50, null=True, blank=True
    )
    main_text_thickness_mobile = models.CharField(
        verbose_name="толщина основного текста (смартфон)", max_length=50, null=True, blank=True
    )
    main_text_color = ColorField(verbose_name="Цвет основного текста", null=True, blank=True)

    class Meta:
        verbose_name = "Кастомные стили"
        verbose_name_plural = "Кастомные стили"
        abstract = True
