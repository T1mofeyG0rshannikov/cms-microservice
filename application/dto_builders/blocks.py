from application.dto.blocks import AdditionalCatalogBlockDTO, MainPageCatalogBlockDTO, PromoCatalogDTO
from infrastructure.persistence.repositories.product_repository import get_product_repository
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.blocks.catalog_block import AdditionalCatalogBlock, MainPageCatalogBlock, PromoCatalog


class MainPageCatalogToBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: MainPageCatalogBlock) -> MainPageCatalogBlockDTO:
        return MainPageCatalogBlockDTO(
            name=block.name,
            template=block.template,
            ancor=block.ancor,
            title=block.title,
            introductory_text=block.introductory_text,
            button_text=block.button_text,
            products=self.pr.get_product_types_for_catalog(block.id)
        )


def get_main_page_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return MainPageCatalogToBlockAssembler(product_repository)


class AdditionalCatalogBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: AdditionalCatalogBlock) -> AdditionalCatalogBlockDTO:
        return AdditionalCatalogBlockDTO(
            name=block.name,
            template=block.template,
            ancor=block.ancor,
            button_text=block.button_text,
            add_annotation=block.add_annotation,
            add_button=block.add_button,
            products=self.pr.get_proudct_types_for_additional_catalog(block.id)
        )


def get_additional_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return AdditionalCatalogBlockAssembler(product_repository)


class PromoCatalogAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: PromoCatalog) -> PromoCatalogDTO:
        return PromoCatalogDTO(
            name=block.name,
            template=block.template,
            ancor=block.ancor,
            title=block.title,
            products=self.pr.get_offers()
        )


def get_promo_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return PromoCatalogAssembler(product_repository)
