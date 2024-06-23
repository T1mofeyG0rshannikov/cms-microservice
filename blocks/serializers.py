from rest_framework import serializers

from blocks.models.blocks_components import CatalogProductType
from blocks.models.catalog_block import MainPageCatalogBlock
from blocks.models.common import Page, Template
from blocks.pages_service.pages_service import PageService
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

        if isinstance(content, MainPageCatalogBlock):
            content.products = [product.product for product in CatalogProductType.objects.filter(block=content)]

        if content is not None:
            content.template.file = "blocks/" + content.template.file

        return content

    def get_styles(self, block):
        styles = self.get_content(block).get_styles()
        if styles is not None:
            return CustomStylesSerializer(styles).data

        return None


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("name", "file")
