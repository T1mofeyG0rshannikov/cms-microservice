from typing import Iterable, Protocol

from domain.materials.document import DocumentInterface, DocumentPatternInterface


class DocumentRepositoryInterface(Protocol):
    def get_document(self, document_slug: str) -> DocumentInterface:
        raise NotImplementedError

    def get_document_patterns(self, document_slug: str) -> Iterable[DocumentPatternInterface]:
        raise NotImplementedError
