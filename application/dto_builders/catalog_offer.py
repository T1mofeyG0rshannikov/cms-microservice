import random

from application.dto.blocks import CatalogOfferPresenterDTO, PromoOfferDTO
from application.formats.date_russian import get_date_in_russian
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.catalog.product_type import ProductType
from infrastructure.persistence.models.catalog.products import Offer
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.security import LinkEncryptor, get_link_encryptor


class OfferAssembler:
    def __init__(self, link_encryptor: LinkEncryptor) -> None:
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


class CatalogOfferAssembler(OfferAssembler):
    def __init__(self, product_repository: ProductRepositoryInterface, link_encryptor: LinkEncryptor) -> None:
        super().__init__(link_encryptor)
        self.r = product_repository

    def process(self, offer: Offer, type: ProductType) -> CatalogOfferPresenterDTO:
        profit = self.r.get_offer_type_relation(type_id=type.id, offer_id=offer.id).profit

        return CatalogOfferPresenterDTO(
            cover=offer.product.cover.url,
            end_promotion=get_date_in_russian(offer.get_end_promotion),
            organization=offer.product.organization.name,
            private=offer.product.private,
            name=offer.product.name,
            link=self.get_link(offer),
            description=offer.description,
            annotation=offer.annotation,
            promotion=offer.promotion,
            profit=profit,
            category=offer.product.category.short,
        )


class PromoOfferAssembler(OfferAssembler):
    def process(self, offer: Offer) -> PromoOfferDTO:
        return PromoOfferDTO.process(offer, link=self.get_link(offer))


def get_promo_offer_assembler(link_encryptor=get_link_encryptor()) -> PromoOfferAssembler:
    return PromoOfferAssembler(link_encryptor)


def get_catalog_offer_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(), link_encryptor=get_link_encryptor()
) -> CatalogOfferAssembler:
    return CatalogOfferAssembler(product_repository=product_repository, link_encryptor=link_encryptor)
