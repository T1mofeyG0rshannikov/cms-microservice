from collections.abc import Iterable
from typing import Protocol

from domain.user.product import UserProductInterface


class UserProductRepositoryInterface(Protocol):
    def filter(self, category_id: int, user_id: int) -> Iterable[UserProductInterface]:
        raise NotImplementedError

    def update_or_create(self, user_id: int, product_id: int, **kwargs) -> tuple[UserProductInterface, bool]:
        raise NotImplementedError

    def update_or_create_user_offer(self, user_id: int, offer_id: int, **kwargs) -> None:
        raise NotImplementedError

    def delete(self, product_id: int) -> None:
        raise NotImplementedError

    def exists(self, user_id: int, product_id: int) -> bool:
        raise NotImplementedError

    def get(self, user_id: int, product_id: int):
        raise NotImplementedError
