from django.core.exceptions import ValidationError
from django.db import models

from utils.errors import Errors

from .get_component import get_component
from .validators import validate_html_filename


class Page(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=50)
    url = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["url"]

    def __str__(self):
        return self.title


class ComponentsName(models.Model):
    name = models.CharField(verbose_name="Имя компонента", max_length=50, unique=True)

    class Meta:
        verbose_name = "Имя компонента"
        verbose_name_plural = "Имена компонентов"

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.ForeignKey(
        ComponentsName, verbose_name="Имя компонента", on_delete=models.CASCADE, related_name="page_component"
    )
    page = models.ForeignKey(Page, related_name="components", verbose_name="Страница", on_delete=models.CASCADE)

    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненты"
        ordering = ["my_order"]

    def __str__(self):
        return str(self.name)


class Template(models.Model):
    name = models.CharField(verbose_name="Название шаблона", max_length=50)
    file = models.CharField(
        verbose_name="Название файла (например base.html)", validators=[validate_html_filename], max_length=50
    )

    class Meta:
        verbose_name = "Html шаблон"
        verbose_name_plural = "Html шаблоны"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not validate_html_filename(self.file):
            raise ValidationError({"file": Errors.incorrect_file_name.value})


class BaseComponent(models.Model):
    template = models.ForeignKey(Template, verbose_name="html шаблон", on_delete=models.CASCADE)
    name = models.ForeignKey(
        ComponentsName,
        verbose_name="Имя компонента",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()
        if get_component(self.name) is not None:
            raise ValidationError({"name": Errors.component_with_name_already_exist.value})


class ExampleComponent(BaseComponent):
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    body = models.TextField(verbose_name="Основной текст", max_length=1000)
    image1 = models.ImageField(verbose_name="Первое изображение", upload_to="images/")
    image2 = models.ImageField(verbose_name="Второе изображение", upload_to="images/")

    class Meta:
        verbose_name = "Контентный блок"
        verbose_name_plural = "Контентные блоки"


class Navbar(BaseComponent):
    title = models.CharField(verbose_name="Заголовок", max_length=100)

    class Meta:
        verbose_name = "навбар"
        verbose_name_plural = "навбар`ы"
