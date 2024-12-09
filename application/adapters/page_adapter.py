from application.adapters.page_block_adapter import BlockAdapter, get_block_adapter
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.blocks.common import Page
from infrastructure.persistence.repositories.page_repository import get_page_repository


class PageAdapter:
    def __init__(self, block_adapter: BlockAdapter, repository: PageRepositoryInterface) -> None:
        self.block_adapter = block_adapter
        self.repository = repository

    def __call__(self, page_model: Page) -> PageInterface:
        block_models = self.repository.get_page_blocks(page_model)

        page_data = {
            "id": page_model.id,
            "title": page_model.title,
            "blocks": [self.block_adapter(block) for block in block_models],
        }

        if hasattr(page_model, "url"):
            page_data["url"] = page_model.url

        return PageInterface(**page_data)


def get_page_adapter(
    block_adapter: BlockAdapter = get_block_adapter(), repository: PageRepositoryInterface = get_page_repository()
) -> PageAdapter:
    return PageAdapter(block_adapter, repository)
