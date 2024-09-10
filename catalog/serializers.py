from rest_framework import serializers

from blocks.models.catalog_block import CatalogBlock
from catalog.models.products import ExclusiveCard, Offer, Product
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
            "add_category",
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
            products = Offer.objects.filter(status="Опубликовано", catalog_product__block=catalog)
        else:
            products = Offer.objects.filter(status="Опубликовано", catalog_product__block=catalog, private=False)

        product_type = catalog.product_type

        return CatalogProductSerializer(products, context={"type": product_type}, many=True).data


class CatalogProductSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    end_promotion = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    promotion = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    private = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "organization",
            "links",
            "link",
            "cover",
            "description",
            "name",
            "private",
            "promotion",
            "profit",
            "end_promotion",
            "category",
        )

    def get_category(self, offer):
        return offer.product.category.short

    def get_name(self, offer):
        return offer.product.name

    def get_description(self, offer):
        return offer.description

    def get_profit(self, offer):
        type = self.context["type"]
        return type.profit

    def get_promotion(self, offer):
        return offer.promotion

    def get_private(self, offer):
        return offer.product.private

    def get_organization(self, offer):
        return offer.product.organization

    def get_link(self, offer):
        return offer.link

    def get_links(self, offer):
        return offer.links.all()

    def get_end_promotion(self, product):
        return get_date_in_russian(product.get_end_promotion)

    def get_cover(self, offer):
        return offer.product.cover.url


class ProductsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "organization", "image", "partner_annotation"]

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
            "partner_bonus",
        ]

    def get_promotion(self, product):
        if product.promotion:
            start_promotion = product.start_promotion.strftime("%d.%m.%Y")
            end_promotion = product.get_end_promotion
            end_promotion = end_promotion.strftime("%d.%m.%Y")

            return f"{start_promotion}-{end_promotion}"

        return "Бессрочно"

    def get_image(self, product):
        return product.cover.url

    def get_name(self, product):
        return f"{product.name} ({product.category})"

    def get_organization(self, product):
        return product.organization.name
