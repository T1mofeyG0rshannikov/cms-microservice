from typing import Protocol

from domain.page_blocks.base_block import BaseBlockInterface
from web.common.models import BlockRelationship


class PageServiceInterface(Protocol):
    def get_page_block(self, blocks_name: BlockRelationship) -> BaseBlockInterface:
        raise NotImplementedError()

    def clone_page(self, page_id: int) -> None:
        raise NotImplementedError()
