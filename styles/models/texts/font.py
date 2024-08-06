from common.models import BaseFont


class Font(BaseFont):
    class Meta:
        verbose_name = "Шрифт"
        verbose_name_plural = "Шрифты"
        ordering = ["name"]
