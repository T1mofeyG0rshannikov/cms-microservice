from dataclasses import dataclass
from datetime import datetime

from domain.products.product import ProductInterface
from domain.user.entities import UserInterface


@dataclass
class UserProductInterface:
    user: UserInterface
    product: ProductInterface
    product_id: int
    connected: datetime | str
    profit: datetime | str
    got: datetime | str
    connected_with_link: bool
    redirections: int

    gain: int

    fully_verified: int
