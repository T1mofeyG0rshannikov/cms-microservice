from django.db.models import Count, Q
from rest_framework import serializers

from blocks.models.catalog_block import AdditionalCatalogBlock, MainPageCatalogBlock
from blocks.models.common import Page
from blocks.pages_service.pages_service import PageService
from catalog.models.product_type import ProductType
from styles.serializers import CustomStylesSerializer


class PageSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "blocks")

    def get_blocks(self, page):
        return BlockSerializer(page.blocks.all(), many=True).data


class BlockSerializer(serializers.Serializer):
    content = serializers.SerializerMethodField()
    styles = serializers.SerializerMethodField()

    page_service = PageService()

    def get_content(self, block):
        content = self.page_service.get_page_block(block.name)
        self.content = content

        if isinstance(content, MainPageCatalogBlock):
            for i in range(1000):
                content.products = ProductType.objects.annotate(
                    count=Count(
                        "catalog_product_types", filter=Q(catalog_product_types__product__status="Опубликовано")
                    )
                ).filter(status="Опубликовано", catalog_product_types__block=content, count__gte=1)

        if isinstance(content, AdditionalCatalogBlock):
            content.products = ProductType.objects.annotate(
                count=Count(
                    "additional_catalog_product_types",
                    filter=Q(additional_catalog_product_types__product__status="Опубликовано"),
                )
            ).filter(status="Опубликовано", additional_catalog_product_types__block=content, count__gte=1)

        if content is not None:
            content.template.file = "blocks/" + content.template.file

        return content

    def get_styles(self, block):
        if not self.content:
            return False

        styles = self.content.get_styles()
        if styles is not None:
            return CustomStylesSerializer(styles).data

        return None
