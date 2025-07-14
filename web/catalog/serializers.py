from rest_framework import serializers

from infrastructure.persistence.models.catalog.products import (
    Product,
)


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
