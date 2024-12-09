from dataclasses import dataclass

from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


@dataclass
class DeleteProductResponse:
    product_name: str


class DeleteUserProduct:
    def __init__(self, repository: ProductRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, user_product_id: int) -> DeleteProductResponse:
        self.repository.delete_user_product(user_product_id)

        return DeleteProductResponse(product_name=self.repository.get_product_name_by_user_products_id(user_product_id))


def get_delete_user_product_interactor(
    repository: ProductRepositoryInterface = get_product_repository(),
) -> DeleteUserProduct:
    return DeleteUserProduct(repository)
