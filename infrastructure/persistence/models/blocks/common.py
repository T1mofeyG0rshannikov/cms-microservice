from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from application.texts.errors import Errors
from infrastructure.persistence.models.common import BasePageBlock, BlockRelationship
from web.blocks.template_exist import is_template_exists
from web.blocks.validators import validate_html_filename


class Page(models.Model):
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
    name = models.ForeignKey(
        BlockRelationship, verbose_name="Блок", on_delete=models.CASCADE, related_name="page_block"
    )
    page = models.ForeignKey(Page, related_name="blocks", verbose_name="Страница", on_delete=models.CASCADE)

    class Meta(BasePageBlock.Meta):
        app_label = "blocks"


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
            raise ValidationError({"file": Errors.incorrect_file_name})
        if not is_template_exists("blocks/" + self.file):
            raise ValidationError({"file": Errors.template_doesnt_exist})


class BaseBlock(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=50, unique=True)
    template = models.ForeignKey(Template, verbose_name="html шаблон", on_delete=models.CASCADE)
    ancor = models.CharField(verbose_name="Якорь", max_length=50, null=True, blank=True)
    block_relation = models.ForeignKey(BlockRelationship, on_delete=models.SET_NULL, null=True)

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        block_relation, _ = BlockRelationship.objects.update_or_create(
            block=f"{type(self).__name__}{self.id}", defaults={"block_name": self.name}
        )

        self.block_relation = block_relation

        super().save(*args, **kwargs)
