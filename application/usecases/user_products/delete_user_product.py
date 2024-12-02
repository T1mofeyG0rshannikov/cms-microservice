from domain.products.repository import ProductRepositoryInterface


class DeleteUserProduct:
    def __init__(self, repository: ProductRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, user_product_id: int) -> None:
        self.repository.delete_user_product(user_product_id)
