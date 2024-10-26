from ckeditor.fields import RichTextField
from django.db import models

from infrastructure.persistence.models.blocks.blocks import (
    FeaturesBlock,
    Footer,
    Navbar,
    QuestionsBlock,
    SocialMediaBlock,
    StagesBlock,
)
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
)
from infrastructure.persistence.models.blocks.mixins import ButtonMixin, TitleMixin
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import Offer
from infrastructure.persistence.models.common import Sortable
from infrastructure.persistence.models.settings import SocialNetwork


class NavMenuItem(ButtonMixin):
    navbar = models.ForeignKey(Navbar, on_delete=models.CASCADE, related_name="menu_items")

    class Meta:
        app_label = "blocks"


class FooterMenuItem(ButtonMixin):
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name="menu_items")

    class Meta:
        app_label = "blocks"


class Feature(TitleMixin):
    icon = models.ImageField(verbose_name="Иконка", upload_to="images/features")
    description = models.TextField(verbose_name="Пояснение")

    ref = models.CharField(verbose_name="ссылка", max_length=500, null=True, blank=True)

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

    class Meta:
        app_label = "blocks"


class SocialMediaButton(models.Model):
    ref = models.CharField(verbose_name="Ссылка на соц. сети", max_length=500)

    social_network = models.ForeignKey(SocialNetwork, on_delete=models.SET_NULL, null=True, verbose_name="Соц. сеть")

    block = models.ForeignKey(SocialMediaBlock, on_delete=models.CASCADE, related_name="buttons")

    class Meta:
        app_label = "blocks"
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"


class Question(TitleMixin):
    text = RichTextField(verbose_name="текст вопроса", max_length=1500)

    block = models.ForeignKey(QuestionsBlock, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        app_label = "blocks"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Stage(TitleMixin):
    text = RichTextField(verbose_name="текст этапа", max_length=1500)
    period = models.CharField(verbose_name="срок этапа", max_length=200)

    num = models.PositiveIntegerField(verbose_name="порядок")

    block = models.ForeignKey(StagesBlock, on_delete=models.CASCADE, related_name="stages")

    class Meta:
        app_label = "blocks"
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"

    def __str__(self):
        return self._meta.verbose_name


class CatalogProduct(Sortable):
    block = models.ForeignKey(CatalogBlock, on_delete=models.CASCADE, related_name="products")
    offer = models.ForeignKey(
        Offer, related_name="catalog_product", on_delete=models.CASCADE, verbose_name="Оффер", null=True
    )

    def __str__(self):
        return str(self.offer)

    class Meta(Sortable.Meta):
        app_label = "blocks"


class CatalogProductType(Sortable):
    block = models.ForeignKey(MainPageCatalogBlock, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductType,
        related_name="catalog_product_types",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        null=True,
    )

    def __str__(self):
        return str(self.product)

    class Meta(Sortable.Meta):
        app_label = "blocks"


class AdditionalCatalogProductType(Sortable):
    block = models.ForeignKey(AdditionalCatalogBlock, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductType,
        related_name="additional_catalog_product_types",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        null=True,
    )

    def __str__(self):
        return str(self.product)

    class Meta(Sortable.Meta):
        app_label = "blocks"
