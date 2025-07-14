import random
from application.dto.blocks import CatalogOfferPresenterDTO
from application.formats.date_russian import get_date_in_russian
from infrastructure.persistence.repositories.product_repository import get_product_repository
from infrastructure.security import LinkEncryptor, get_link_encryptor
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import Offer
from domain.products.repository import ProductRepositoryInterface


class CatalogOfferAssembler:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        link_encryptor: LinkEncryptor
    ) -> None:
        self.r = product_repository
        self.link_encryptor = link_encryptor

    def get_link(self, offer: Offer):   
        links = offer.links.all()

        link_change = []

        for link in links:
            link_change.append(link.percent / 100)

        if link_change:
            link = random.choices(links, weights=link_change, k=1)[0].text
            link = self.link_encryptor.encrypt(link)

            return link

        return ""

    def build_data(self, offer: Offer, type: ProductType) -> CatalogOfferPresenterDTO:
        profit = self.r.get_offer_type_relation(type_id=type.id, offer_id=offer.id).profit
    
        return CatalogOfferPresenterDTO(
            cover=offer.product.cover.url,
            end_promotion=get_date_in_russian(offer.get_end_promotion),
            links=offer.links.all(),
            organization=offer.product.organization,
            private=offer.product.private,
            name=offer.product.name,
            link=self.get_link(offer),
            description=offer.description,
            annotation=offer.annotation,
            promotion=offer.promotion,
            profit=profit,
            category=offer.product.category.short
        )


def get_catalog_offer_assembler(
    product_repository: ProductRepositoryInterface=get_product_repository(), 
    link_encryptor=get_link_encryptor()
) -> CatalogOfferAssembler:
    return CatalogOfferAssembler(
        product_repository=product_repository,
        link_encryptor=link_encryptor
    )
