from collections.abc import Iterable
from dataclasses import dataclass

from domain.page_blocks.entities.base_block import PageBlockInterface


@dataclass
class PageInterface:
    id: int
    blocks: Iterable[PageBlockInterface]
    url: str | None = None
    title: str = None
    ancor: str = None
