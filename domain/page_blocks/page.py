from dataclasses import dataclass


@dataclass
class PageInterface:
    id: int
    url: str | None
