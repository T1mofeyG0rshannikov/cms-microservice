from application.dto.user_products import DeleteProductResponse
from domain.products.repository import ProductRepositoryInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)


class DeleteUserProduct:
    def __init__(
        self, product_repository: ProductRepositoryInterface, user_product_repository: UserProductRepositoryInterface
    ) -> None:
        self.product_repository = product_repository
        self.user_product_repository = user_product_repository

    def __call__(self, user_product_id: int) -> DeleteProductResponse:
        self.user_product_repository.delete(user_product_id)
        product = self.product_repository.get(user_product_id=user_product_id)

        return DeleteProductResponse(product_name=product.name if product else None)


def get_delete_user_product_interactor(
    repository: ProductRepositoryInterface = get_product_repository(),
    user_product_repository: UserProductRepositoryInterface = get_user_product_repository(),
) -> DeleteUserProduct:
    return DeleteUserProduct(repository, user_product_repository)
