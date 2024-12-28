from dataclasses import dataclass

from domain.common.replacement_pattern import ReplacementPatternInterface


@dataclass
class DocumentInterface:
    text: str
    name: str
    title: str | None = None
    slug: str | None = None


@dataclass
class DocumentPatternInterface(ReplacementPatternInterface):
    pass
