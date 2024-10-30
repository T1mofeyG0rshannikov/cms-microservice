from typing import Protocol

from domain.materials.document import DocumentInterface


class DocumentRepositoryInterface(Protocol):
    def get_document(self, document_slug: str) -> DocumentInterface:
        raise NotImplementedError

    def get_document_patterns(self, document_slug: str):
        raise NotImplementedError
