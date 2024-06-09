import datetime
import random

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from blocks.models.catalog_block import CatalogBlock
from catalog.models.products import Product


class CatalogBlockSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()

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
        )

    def get_template(self, catalog):
        template = catalog.template
        template.file = "blocks/" + template.file

        return template

    def get_products(self, catalog):
        products = [catalog_product.product for catalog_product in catalog.products.all()]

        return CatalogProductSerializer(products, many=True).data


class CatalogProductSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
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

        month = date.month
        day = date.day
        year = date.year

        months = [
            "января",
            "февраля",
            "марта",
            "апреля",
            "мая",
            "июня",
            "июля",
            "августа",
            "сентября",
            "октября",
            "ноября",
            "декабря",
        ]

        return f"{day} {months[month - 1]} {year}"

    def get_cover(self, product):
        return product.cover.url

    def get_link(self, product):
        links = product.links.all()

        link_change = []

        for i in range(len(links)):
            for j in range(links[i].percent):
                link_change.append(i)

        return links[random.choice(link_change)].text
