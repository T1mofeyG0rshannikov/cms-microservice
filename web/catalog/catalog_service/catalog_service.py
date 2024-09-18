from typing import Any

from domain.user.interfaces import UserInterface
from web.blocks.models.blocks import Cover
from web.blocks.models.catalog_block import CatalogBlock
from web.blocks.pages_service.page_service_interface import PageServiceInterface
from web.blocks.pages_service.pages_service import get_page_service
from web.blocks.serializers import PageSerializer
from web.catalog.catalog_service.catalog_service_interface import (
    CatalogServiceInterface,
)
from web.catalog.models.blocks import CatalogPageTemplate
from web.catalog.models.product_type import ProductType
from web.catalog.serializers import CatalogBlockSerializer
from web.common.models import BlockRelationship
from web.styles.models.styles.styles import CatalogCustomStyles
from web.styles.serializers import CustomStylesSerializer


class CatalogService(CatalogServiceInterface):
    def __init__(self, page_service: PageServiceInterface):
        self.page_service = page_service

    def set_page_title(self, serialized_page, slug: str):
        serialized_page["title"] = ProductType.objects.values("name").get(slug=slug)["name"]

        return serialized_page

    def get_page(self, user: UserInterface, slug: str):
        page = CatalogPageTemplate.objects.prefetch_related("blocks").first()

        page = self.set_catalog_block(page, user, slug)
        page = self.set_catalog_cover(page, slug)
        page = self.set_page_title(page, slug)

        return page

    def get_catalog_block(self, user: UserInterface, slug: str) -> dict[str, Any]:
        catalog = CatalogBlock.objects.prefetch_related("styles").get(product_type__slug=slug)
        catalog_relation = BlockRelationship.objects.get(block_name=catalog.name)
        catalog = self.page_service.get_page_block(catalog_relation)
        styles = catalog.get_styles()

        if styles is None:
            styles = CatalogCustomStyles.objects.create(block=catalog)

        catalog_styles = CustomStylesSerializer(styles).data

        catalog = CatalogBlockSerializer(catalog, context={"user": user}).data

        return {"content": catalog, "styles": catalog_styles}

    def get_catalog_cover(self, slug: str):
        cover = Cover.objects.values("name").get(producttype__slug=slug)
        cover_relation = BlockRelationship.objects.get(block_name=cover["name"])

        cover = self.page_service.get_page_block(cover_relation)
        cover.template.file = "blocks/" + cover.template.file

        cover_styles = CustomStylesSerializer(cover.get_styles()).data

        return {"content": cover, "styles": cover_styles}

    def set_catalog_block(self, page, user: UserInterface, slug: str) -> dict[Any, Any]:
        page = PageSerializer(page).data
        catalog = self.get_catalog_block(user, slug)

        for block in page["blocks"]:
            if isinstance(block["content"], CatalogBlock):
                page["blocks"][page["blocks"].index(block)] = catalog

        return page

    def set_catalog_cover(self, serialized_page, slug: str):
        cover = self.get_catalog_cover(slug)

        for block in serialized_page["blocks"]:
            if isinstance(block["content"], Cover):
                serialized_page["blocks"][serialized_page["blocks"].index(block)] = cover

        return serialized_page


def get_catalog_service() -> CatalogService:
    return CatalogService(get_page_service())
