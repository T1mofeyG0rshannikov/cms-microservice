from typing import Any

from domain.products.repository import ProductRepositoryInterface


class AddUserProduct:
    def __init__(self, repository: ProductRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, fields: dict[str, Any], user_id: int) -> None:
        product = fields.get("product")

        self.repository.update_or_create_user_product(
            comment=fields.get("comment"),
            connected=fields.get("connected"),
            profit=fields.get("profit"),
            got=fields.get("got"),
            screen=fields.get("screen"),
            connected_with_link=fields.get("connected_with_link") == "true",
            deleted=False,
            product_id=product,
            user_id=user_id,
        )

        link = fields.get("link")
        if link:
            offers = self.repository.get_product_offers(product)
            for offer in offers:
                self.repository.update_or_create_user_offer(offer_id=offer.id, user_id=user_id, link=link)
