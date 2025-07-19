from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.utils import get_model_class_by_str
from infrastructure.persistence.repositories.page_repository import get_page_repository


class CloneBlock:
    def __init__(self, page_repository: PageRepositoryInterface) -> None:
        self.r = page_repository

    def __call__(self, block_id: int, block_class_name: str) -> None:
        block_class = get_model_class_by_str(block_class_name)

        self.r.clone_block(block_id, block_class)


def get_clone_block(page_repository: PageRepositoryInterface = get_page_repository()) -> CloneBlock:
    return CloneBlock(page_repository=page_repository)
