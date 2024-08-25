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
            return ExclusiveCard.objects.first()

    def get_template(self, catalog):
        template = catalog.template
        template.file = "blocks/" + template.file

        return template

    def get_products(self, catalog):
        user = self.context["user"]

        if user.is_authenticated:
            products = Product.objects.filter(status="Опубликовано", catalog_product__block=catalog)
        else:
            products = Product.objects.filter(status="Опубликовано", catalog_product__block=catalog, private=False)

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
        return get_date_in_russian(product.get_end_date)

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


class ProductsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "organization", "image"]

    def get_image(self, product):
        return product.cover.url

    def get_name(self, product):
        return f"{product.name} ({product.category})"

    def get_organization(self, product):
        return product.organization.name


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    promotion = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "organization",
            "image",
            "profit",
            "promotion",
            "partner_description",
            "partner_annotation",
        ]

    def get_promotion(self, product):
        if product.promotion:
            start_promotion = product.start_promotion.strftime("%d.%m.%Y")
            end_promotion = product.get_end_promotion
            end_promotion = end_promotion.strftime("%d.%m.%Y")

            return f"{start_promotion}-{end_promotion}"

        return "-"

    def get_image(self, product):
        return product.cover.url

    def get_name(self, product):
        return f"{product.name} ({product.category})"

    def get_organization(self, product):
        return product.organization.name
