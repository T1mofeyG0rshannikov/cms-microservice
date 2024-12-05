from collections.abc import Iterable

from django.db.models import Case, When

from domain.page_blocks.entities.base_block import (
    CatalogBlockInterface,
    PageBlockInterface,
)
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.files.files import find_class_in_directory
from infrastructure.persistence.models.blocks.blocks import Cover
from infrastructure.persistence.models.blocks.catalog_block import CatalogBlock
from infrastructure.persistence.models.blocks.common import BaseBlock, Block, Page
from infrastructure.persistence.models.catalog.blocks import Block as CatalogPageBlock
from infrastructure.persistence.models.catalog.blocks import (
    BlockRelationship as CatalogBlockRelationship,
)
from infrastructure.persistence.models.catalog.blocks import CatalogPageTemplate
from infrastructure.persistence.models.common import BlockRelationship


class PageRepository(PageRepositoryInterface):
    def get_catalog_block(self, slug: str) -> CatalogBlockInterface:
        return CatalogBlock.objects.get(product_type__slug=slug)

    def get_page_by_id(self, id: int) -> PageInterface:
        return Page.objects.get(id=id)

    def get_page_by_url(self, url: str) -> PageInterface:
        try:
            return Page.objects.get(url=url)
        except Page.DoesNotExist:
            return None

    def get_page_blocks(self, page_model) -> Iterable[BaseBlock]:
        if isinstance(page_model, Page):
            block_class = Block
            block_relation_class = BlockRelationship

        elif isinstance(page_model, CatalogPageTemplate):
            block_class = CatalogPageBlock
            block_relation_class = CatalogBlockRelationship

        block_names = block_class.objects.filter(page=page_model).order_by("my_order").values_list("name", flat=True)
        blocks = (
            block_relation_class.objects.filter(id__in=block_names)
            .order_by(Case(*[When(id=id, then=pos) for pos, id in enumerate(block_names)]))
            .values("block_name", "block")
        )

        block_models = []
        for block in blocks:
            ind = len(block["block"])
            while block["block"][ind - 1].isdigit() and block["block"][ind - 2].isdigit():
                ind -= 1

            block_class: BaseBlock = find_class_in_directory(
                "infrastructure/persistence/models/blocks", block["block"][0 : ind - 1]
            )
            block_id = int(block["block"][ind - 1 : :])

            block_models.append(block_class.objects.get(id=block_id))

        return block_models

    def clone_page(self, page_id: int) -> None:
        page = self.get_page_by_id(page_id)
        blocks = page.blocks.all()
        print(blocks)

        page.pk = None

        page.save()

        for block in blocks:
            block.pk = None
            block.page = page
            block.save()

    def get_catalog_page_template(self) -> PageInterface:
        return CatalogPageTemplate.objects.first()

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        return Cover.objects.get(producttype__slug=slug)


def get_page_repository() -> PageRepositoryInterface:
    return PageRepository()
