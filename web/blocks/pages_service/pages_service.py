from domain.page_blocks.base_block import BaseBlockInterface
from infrastructure.persistence.models.blocks.common import BaseBlock, Page
from web.blocks.pages_service.page_service_interface import PageServiceInterface
from web.common.models import BlockRelationship


class PageService(PageServiceInterface):
    def get_page_block(self, blocks_name: BlockRelationship) -> BaseBlockInterface:
        block = None

        for f in blocks_name._meta.related_objects:
            if isinstance(f.related_model.objects.first(), BaseBlock):
                if f.field.model.objects.filter(block_relation=blocks_name).exists():
                    block = f.field.model.objects.select_related("styles").get(block_relation_id=blocks_name.id)
                    break

        return block

    def clone_page(self, page_id: int) -> None:
        page = Page.objects.get(id=page_id)
        blocks = page.blocks.all()
        print(blocks)

        page.pk = None

        page.save()

        for block in blocks:
            block.pk = None
            block.page = page
            block.save()


def get_page_service() -> PageServiceInterface:
    return PageService()
