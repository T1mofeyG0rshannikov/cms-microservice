from django.db import models


class BaseFormatterPattern(models.Model):
    tag = models.CharField(verbose_name="Тэг", max_length=50)
    text = models.CharField(verbose_name="Текст", max_length=50)

    METHODS = [("openUserForm", "openUserForm"), ("openUpdateProductForm", "openUpdateProductForm")]
    method = models.CharField(verbose_name="Метод", choices=METHODS, max_length=50, null=True, blank=True)
    arg = models.CharField(verbose_name="Аргумент", null=True, blank=True, max_length=50)

    class Meta:
        abstract = True
        verbose_name = "Подстановочные шаблоны"
        verbose_name_plural = "Подстановочные шаблоны"

    def __str__(self):
        return ""
