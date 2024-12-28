from domain.materials.document import DocumentInterface
from domain.materials.repository import DocumentRepositoryInterface
from infrastructure.persistence.repositories.document_repository import (
    get_document_repository,
)


class FormatDocument:
    def __init__(self, repository: DocumentRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, document_slug: str) -> DocumentInterface | None:
        document = self.repository.get(document_slug)
        if not document:
            return None

        document_text = document.text

        patterns = self.repository.get_document_patterns(document_slug)

        for pattern in patterns:
            if pattern.method:
                arg = ""
                if pattern.arg:
                    if pattern.arg.isdigit():
                        arg = pattern.arg
                    else:
                        arg = f'''"{pattern.arg}"'''

                string = f"""<a class="ref" onclick="{pattern.method}({arg})">{pattern.text}</a>"""
            else:
                string = pattern.text

            document_text = document_text.replace(pattern.tag, string)

        return DocumentInterface(text=document_text, name=document.name)


def get_format_document(document_repository: DocumentRepositoryInterface = get_document_repository()) -> FormatDocument:
    return FormatDocument(repository=document_repository)
