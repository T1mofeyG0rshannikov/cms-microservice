from collections.abc import Iterable

from django.db.models import Q

from domain.user.product import UserProductInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.models.user.product import UserOffer, UserProduct


class UserProductRepository(UserProductRepositoryInterface):
    def filter(self, category_id: int, user_id: int) -> Iterable[UserProductInterface]:
        filters = Q(user_id=user_id, deleted=False)

        if category_id:
            filters &= Q(product__category_id=category_id)

        return UserProduct.objects.filter(filters)

    def update_or_create(self, user_id: int, product_id: int, **kwargs) -> tuple[UserProductInterface, bool]:
        product, created = UserProduct.objects.update_or_create(user_id=user_id, product_id=product_id, defaults=kwargs)

        return product, created

    def update_or_create_user_offer(self, user_id: int, offer_id: int, **kwargs) -> None:
        UserOffer.objects.update_or_create(user_id=user_id, offer_id=offer_id, defaults=kwargs)

    def delete(self, product_id: int) -> None:
        UserProduct.objects.filter(id=product_id).update(deleted=True)

    def exists(self, user_id: int, product_id: int) -> bool:
        return UserProduct.objects.filter(user_id=user_id, product_id=product_id, deleted=False).exists()

    def get(self, user_id: int, product_id: int):
        return UserProduct.objects.get(user_id=user_id, product_id=product_id)


def get_user_product_repository() -> UserProductRepositoryInterface:
    return UserProductRepository()
