from collections.abc import Iterable
from typing import Protocol

from domain.materials.document import DocumentInterface, DocumentPatternInterface


class DocumentRepositoryInterface(Protocol):
    def get(self, document_slug: str) -> DocumentInterface:
        raise NotImplementedError

    def get_document_patterns(self, document_slug: str) -> Iterable[DocumentPatternInterface]:
        raise NotImplementedError

    def all(self) -> Iterable[DocumentInterface]:
        raise NotImplementedError
