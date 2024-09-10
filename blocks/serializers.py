from rest_framework import serializers

from blocks.models.catalog_block import AdditionalCatalogBlock, MainPageCatalogBlock
from blocks.models.common import Page
from blocks.pages_service.pages_service import PageService
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
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
    repository = get_product_repository()

    def get_content(self, block):
        content = self.page_service.get_page_block(block.name)
        self.content = content

        if isinstance(content, MainPageCatalogBlock):
            content.products = self.repository.get_product_types_for_catalog(content.id)

        if isinstance(content, AdditionalCatalogBlock):
            content.products = self.repository.get_proudct_types_for_additional_catalog(content.id)

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
