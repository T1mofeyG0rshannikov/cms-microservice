from blocks.models.common import BaseBlock, BlockRelationship, Page
from blocks.pages_service.page_service_interface import PageServiceInterface


class PageService(PageServiceInterface):
    def get_page_block(self, blocks_name: BlockRelationship) -> BaseBlock:
        blocks = [
            f.field.model.objects.filter(block_relation=blocks_name).first()
            for f in blocks_name._meta.get_fields()
            if (f.one_to_many or f.one_to_one) and isinstance(f.field.model.objects.first(), BaseBlock)
        ]

        if blocks:
            block = [block for block in blocks if block is not None][0]
        else:
            block = None

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


def get_page_service() -> PageService:
    return PageService()
