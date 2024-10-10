from dataclasses import dataclass

from domain.page_blocks.base_block import BaseBlockInterface


@dataclass
class PageInterface:
    id: int
    blocks: list[BaseBlockInterface]
    url: str | None = None
    title: str = None
    ancor: str = None
