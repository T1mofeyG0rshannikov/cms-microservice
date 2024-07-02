from ckeditor.fields import RichTextField
from django.db import models

from blocks.models.blocks import (
    FeaturesBlock,
    Navbar,
    QuestionsBlock,
    SocialMediaBlock,
    StagesBlock,
)
from blocks.models.mixins import ButtonMixin, TitleMixin
from catalog.models.products import Product
from common.models import SocialNetwork, Sortable


class NavMenuItem(ButtonMixin):
    navbar = models.ForeignKey(Navbar, on_delete=models.SET_NULL, null=True, related_name="menu_items")


class Feature(TitleMixin):
    icon = models.ImageField(verbose_name="Иконка", upload_to="images/features")
    description = models.TextField(verbose_name="Пояснение")
    block = models.ForeignKey(
        FeaturesBlock, verbose_name="Блок", on_delete=models.SET_NULL, null=True, related_name="features"
    )

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        try:
            this = Feature.objects.get(id=self.id)
            if this.icon != self.icon:
                this.icon.delete()
        except Exception:
            pass
        super().save(*args, **kwargs)


class SocialMediaButton(models.Model):
    ref = models.CharField(verbose_name="Ссылка на соц. сети", max_length=500)

    social_network = models.ForeignKey(SocialNetwork, on_delete=models.SET_NULL, null=True, verbose_name="Соц. сеть")

    block = models.ForeignKey(SocialMediaBlock, on_delete=models.CASCADE, related_name="buttons")

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"


class Question(TitleMixin):
    text = RichTextField(verbose_name="текст вопроса", max_length=1500)

    block = models.ForeignKey(QuestionsBlock, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Stage(TitleMixin):
    text = RichTextField(verbose_name="текст этапа", max_length=1500)
    period = models.CharField(verbose_name="срок этапа", max_length=200)

    num = models.PositiveIntegerField(verbose_name="порядок")

    block = models.ForeignKey(StagesBlock, on_delete=models.CASCADE, related_name="stages")

    class Meta:
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"

    def __str__(self):
        return self._meta.verbose_name


class CatalogProduct(Sortable):
    block = models.ForeignKey("blocks.CatalogBlock", on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", null=True)

    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        self.product.status = "Опубликовано"
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.status = "Новое"
        self.product.save()

        super().delete(*args, **kwargs)


class CatalogProductType(Sortable):
    block = models.ForeignKey("blocks.MainPageCatalogBlock", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.ProductType", on_delete=models.CASCADE, verbose_name="Продукт", null=True)

    def __str__(self):
        return str(self.product)

    """def save(self, *args, **kwargs):
        self.product.status = "Опубликовано"
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.status = "Новое"
        self.product.save()

        super().delete(*args, **kwargs)"""
