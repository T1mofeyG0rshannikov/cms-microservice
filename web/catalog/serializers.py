from rest_framework import serializers

from application.formats.date_russian import get_date_in_russian
from infrastructure.persistence.models.catalog.products import (
    OfferTypeRelation,
    Product,
)


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
    annotation = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "organization",
            "links",
            "link",
            "cover",
            "description",
            "annotation",
            "name",
            "private",
            "promotion",
            "profit",
            "end_promotion",
            "category",
        )

    def get_annotation(self, offer):
        return offer.annotation

    def get_category(self, offer):
        return offer.product.category.short

    def get_name(self, offer):
        return offer.product.name

    def get_description(self, offer):
        return offer.description

    def get_profit(self, offer):
        type = self.context["type"]
        return OfferTypeRelation.objects.get(type=type, offer=offer).profit

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
            "promotion",
            "partner_description",
            "partner_annotation",
            "partner_bonus",
        ]

    def get_promotion(self, product):
        offer = product.offers.filter(partner_program="Пригласи друга").first()

        if offer:
            return offer.get_end_promotion.strftime("%d.%m.%Y")

        for offer in product.offers.all():
            if offer.end_promotion:
                return offer.get_end_promotion.strftime("%d.%m.%Y")

        return "Бессрочно"

    def get_image(self, product):
        return product.cover.url

    def get_name(self, product):
        return f"{product.name} ({product.category})"

    def get_organization(self, product):
        return product.organization.name
