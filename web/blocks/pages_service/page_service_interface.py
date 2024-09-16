from typing import Protocol

from web.blocks.models.common import BaseBlock, BlockRelationship


class PageServiceInterface(Protocol):
    def get_page_block(self, blocks_name: BlockRelationship) -> BaseBlock:
        raise NotImplementedError()

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError()
