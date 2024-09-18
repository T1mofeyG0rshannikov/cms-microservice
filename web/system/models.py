from django.db import models


class Email(models.Model):
    email = models.CharField(verbose_name="почта", max_length=200)

    class Meta:
        verbose_name = "Системная почта"
        verbose_name_plural = "Системные почты"
