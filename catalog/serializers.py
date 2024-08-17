import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from blocks.models.catalog_block import CatalogBlock
from catalog.models.product_type import ProductType
from catalog.models.products import ExclusiveCard, Product
from utils.date_russian import get_date_in_russian


class CatalogBlockSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()
    exclusive_card = serializers.SerializerMethodField()

    class Meta:
        model = CatalogBlock
        fields = (
            "title",
            "template",
            "button_text",
            "button_ref",
            "product_type",
            "introductory_text",
            "add_exclusive",
            "products",
            "exclusive_card",
        )

    def get_exclusive_card(self, catalog):
        if catalog.add_exclusive:
            return ExclusiveCard.objects.all().first()

    def get_template(self, catalog):
        template = catalog.template
        template.file = "blocks/" + template.file

        return template

    def get_products(self, catalog):
        user = self.context["user"]

        if user.is_authenticated:
            products = [catalog_product.product for catalog_product in catalog.products.all()]
        else:
            products = filter(
                lambda product: not product.private,
                [catalog_product.product for catalog_product in catalog.products.all()],
            )

        return CatalogProductSerializer(products, many=True).data


class CatalogProductSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    end_promotion = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "organization",
            "links",
            "link",
            "cover",
            "name",
            "type",
            "annotation",
            "description",
            "banner",
            "private",
            "promotion",
            "profit",
            "end_promotion",
        )

    def get_organization(self, product):
        return product.organization

    def get_end_promotion(self, product):
        date = product.end_promotion
        if date is None:
            date = datetime.date.today() + relativedelta(years=+1)

        return get_date_in_russian(date)

    def get_cover(self, product):
        return product.cover.url


class MainPageCatalogProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ("name", "description", "url")


class MainPageCatalogBlockSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()

    class Meta:
        model = CatalogBlock
        fields = (
            "template",
            "button_text",
            "button_ref",
            "products",
        )

    def get_template(self, catalog):
        template = catalog.template
        template.file = "blocks/" + template.file

        return template

    def get_products(self, catalog):
        products = [catalog_product.product for catalog_product in catalog.products.all()]

        return MainPageCatalogProductSerializer(products, many=True).data
