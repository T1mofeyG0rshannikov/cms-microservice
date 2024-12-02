from dataclasses import dataclass

from domain.page_blocks.base_block import PageBlockInterface


@dataclass
class PageInterface:
    id: int
    blocks: list[PageBlockInterface]
    url: str | None = None
    title: str = None
    ancor: str = None
