from domain.page_blocks.base_block import BaseBlockInterface
from domain.page_blocks.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.blocks.common import BaseBlock, Page
from infrastructure.persistence.models.common import BlockRelationship


class PageRepository(PageRepositoryInterface):
    def get_page_by_id(self, id: int) -> PageInterface:
        return Page.objects.get(id=id)

    def get_page_by_url(self, url: str) -> PageInterface:
        try:
            return Page.objects.prefetch_related("blocks").get(url=url)
        except Page.DoesNotExist:
            return None

    def get_page_block(self, blocks_name: str) -> BaseBlockInterface:
        block = None

        blocks_name = BlockRelationship.objects.get(block_name=blocks_name)

        for f in blocks_name._meta.related_objects:
            if isinstance(f.related_model.objects.first(), BaseBlock):
                if f.field.model.objects.filter(block_relation=blocks_name).exists():
                    block = f.field.model.objects.select_related("styles").get(block_relation_id=blocks_name.id)
                    break

        return block

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


def get_page_repository() -> PageRepositoryInterface:
    return PageRepository()
