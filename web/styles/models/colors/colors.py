from colorfield.fields import ColorField

from web.styles.models.colors.base_color import BaseColor
from web.styles.models.styles.base_styles import BaseStyles


class ColorStyles(BaseStyles):
    main_color = ColorField(verbose_name="Основной цвет", default="#FFFFFF")
    secondary_color = ColorField(verbose_name="Вторичный цвет", default="#FFFFFF")
    background_color = ColorField(verbose_name="Цвет фона", default="#FFFFFF")
    second_background_color = ColorField(verbose_name="Цвет фона 2", default="#FFFFFF")

    class Meta:
        verbose_name = "Цвета"
        verbose_name_plural = "Цвета"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        main_color, _ = BaseColor.objects.update_or_create(name="main_color", defaults={"color": self.main_color})
        secondary_color, _ = BaseColor.objects.update_or_create(
            name="secondary_color", defaults={"color": self.secondary_color}
        )
        background_color, _ = BaseColor.objects.update_or_create(
            name="background_color", defaults={"color": self.background_color}
        )
        second_background_color, _ = BaseColor.objects.update_or_create(
            name="second_background_color", defaults={"color": self.second_background_color}
        )

        super().save(*args, **kwargs)
