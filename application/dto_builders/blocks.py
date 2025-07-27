from application.dto.blocks import (
    AdditionalCatalogBlockDTO,
    CatalogDTO,
    MainPageCatalogBlockDTO,
    PromoCatalogDTO,
)
from application.dto_builders.catalog_offer import (
    CatalogOfferAssembler,
    PromoOfferAssembler,
    get_catalog_offer_assembler,
    get_promo_offer_assembler,
)
from application.mappers.products import from_orm_to_product_type
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.db_filters.products import OffersFilter
from infrastructure.persistence.models.blocks.catalog_block import (
    AdditionalCatalogBlock,
    CatalogBlock,
    MainPageCatalogBlock,
    PromoCatalog,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class MainPageCatalogToBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def process(self, block: MainPageCatalogBlock) -> MainPageCatalogBlockDTO:
        return MainPageCatalogBlockDTO.process(
            block, products=[from_orm_to_product_type(type) for type in self.pr.get_product_types_for_catalog(block.id)]
        )


def get_main_page_catalog_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(),
) -> MainPageCatalogToBlockAssembler:
    return MainPageCatalogToBlockAssembler(product_repository)


class AdditionalCatalogBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def process(self, block: AdditionalCatalogBlock) -> AdditionalCatalogBlockDTO:
        return AdditionalCatalogBlockDTO.process(
            block,
            products=[
                from_orm_to_product_type(type) for type in self.pr.get_proudct_types_for_additional_catalog(block.id)
            ],
        )


def get_additional_catalog_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(),
) -> AdditionalCatalogBlockAssembler:
    return AdditionalCatalogBlockAssembler(product_repository)


class PromoCatalogAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface, offer_builder: PromoOfferAssembler) -> None:
        self.pr = product_repository
        self.builder = offer_builder

    def process(self, block: PromoCatalog) -> PromoCatalogDTO:
        return PromoCatalogDTO.process(
            block,
            products=[self.builder.process(offer) for offer in self.pr.filter_offers()],
        )


def get_promo_catalog_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(),
    offer_builder: PromoCatalogAssembler = get_promo_offer_assembler(),
) -> PromoCatalogAssembler:
    return PromoCatalogAssembler(product_repository, offer_builder)


class CatalogAssembler:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        product_assembler: CatalogOfferAssembler,
    ) -> None:
        self.pr = product_repository
        self.product_assembler = product_assembler

    def process(self, block: CatalogBlock) -> CatalogDTO:
        type = block.product_type

        private = None
        if hasattr(block, "user_is_authenticated"):
            private = block.user_is_authenticated

        products = self.pr.get_catalog_offers(OffersFilter(private=private, product_type_slug=type.slug))

        products = [self.product_assembler.process(offer, type) for offer in products]

        return CatalogDTO.process(
            block,
            exclusive_card=self.pr.get_exclusive_card() if block.add_exclusive else None,
            products=products,
        )


def get_catalog_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(),
    product_assembler: CatalogOfferAssembler = get_catalog_offer_assembler(),
) -> CatalogAssembler:
    return CatalogAssembler(product_repository, product_assembler)
