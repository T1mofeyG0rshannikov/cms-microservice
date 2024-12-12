from datetime import datetime

from domain.products.repository import ProductRepositoryInterface
from domain.user.exceptions import LinkOrConnectedRequired
from domain.user.product import UserProductInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)


class AddUserProduct:
    def __init__(
        self, product_repository: ProductRepositoryInterface, user_product_repository: UserProductRepositoryInterface
    ) -> None:
        self.product_repository = product_repository
        self.user_product_repository = user_product_repository

    def __call__(
        self,
        user_id: int,
        product_id: int,
        comment: str = None,
        connected: datetime = None,
        got: datetime = None,
        screen: str = None,
        connected_with_link: str = None,
        profit: datetime = None,
        link: str = None,
    ) -> tuple[UserProductInterface, bool]:
        if not link and not connected:
            raise LinkOrConnectedRequired("Укажите вашу партнерскую ссылку или дату оформления продукта")

        if link:
            offers = self.product_repository.get_product_offers(product_id)
            for offer in offers:
                self.user_product_repository.update_or_create_user_offer(offer_id=offer.id, user_id=user_id, link=link)

        return self.user_product_repository.update_or_create(
            comment=comment,
            connected=connected,
            profit=profit,
            got=got,
            screen=screen,
            connected_with_link=connected_with_link == "true",
            deleted=False,
            product_id=product_id,
            user_id=user_id,
        )


def get_add_product_interactor(
    repository: ProductRepositoryInterface = get_product_repository(),
    user_product_repository: UserProductRepositoryInterface = get_user_product_repository(),
) -> AddUserProduct:
    return AddUserProduct(repository, user_product_repository)
