from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from application.texts.errors import ErrorsMessages
from web.blocks.template_exist import is_template_exists
from web.blocks.validators import validate_html_filename


class BasePageModel(models.Model):
    class Meta:
        abstract = True


class Template(models.Model):
    name = models.CharField(verbose_name="Название шаблона", max_length=50)
    file = models.CharField(verbose_name="Название файла (например base.html)", max_length=50)

    class Meta:
        app_label = "blocks"
        verbose_name = "шаблон"
        verbose_name_plural = "шаблоны"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not validate_html_filename(self.file):
            raise ValidationError({"file": ErrorsMessages.incorrect_file_name})
        if not is_template_exists("blocks/" + self.file):
            raise ValidationError({"file": ErrorsMessages.template_doesnt_exist})


class BaseBlock(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=50, unique=True)
    template = models.ForeignKey(Template, verbose_name="html шаблон", on_delete=models.CASCADE)
    ancor = models.CharField(verbose_name="Якорь", max_length=50, null=True, blank=True)

    class Meta:
        app_label = "blocks"
        abstract = True

    def __str__(self):
        return self.name

    def get_styles(self):
        try:
            return self.styles
        except ObjectDoesNotExist:
            return None


class Sortable(models.Model):
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ["my_order"]


class BasePageBlock(Sortable):
    class Meta(Sortable.Meta):
        abstract = True
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"


class BaseFont(models.Model):
    name = models.CharField(verbose_name="Имя шрифта", max_length=50)
    link = models.CharField(verbose_name="Ссылка для подключения", max_length=250, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Page(BasePageModel):
    title = models.CharField(verbose_name="Заголовок", max_length=50)
    url = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = "blocks"
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["url"]

    def __str__(self):
        return self.title


class Block(BasePageBlock):
    page = models.ForeignKey(Page, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    block_id = models.PositiveIntegerField(null=True)
    block = GenericForeignKey("content_type", "block_id")

    class Meta(BasePageBlock.Meta):
        app_label = "blocks"

    def __str__(self):
        return str(self.block)
