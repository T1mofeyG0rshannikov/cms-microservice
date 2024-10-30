from dataclasses import dataclass


@dataclass
class DocumentInterface:
    text: str
    name: str
    title: str = None
    slug: str = None
