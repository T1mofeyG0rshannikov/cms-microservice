import os
from application.dto.blocks import AdditionalCatalogBlockDTO, CatalogDTO, MainPageCatalogBlockDTO, OfferDTO, PromoCatalogDTO
from application.dto_builders.catalog_offer import CatalogOfferAssembler, get_catalog_offer_assembler
from application.mappers.products import from_orm_to_product_type
from infrastructure.public.template_settings import TemplateSettings, get_template_settings
from infrastructure.persistence.repositories.product_repository import get_product_repository
from domain.products.repository import ProductRepositoryInterface
from infrastructure.persistence.models.blocks.catalog_block import AdditionalCatalogBlock, CatalogBlock, MainPageCatalogBlock, PromoCatalog


class MainPageCatalogToBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: MainPageCatalogBlock, config: TemplateSettings = get_template_settings()) -> MainPageCatalogBlockDTO:
        return MainPageCatalogBlockDTO(
            name=block.name,
            template=os.path.join(config.blocks_templates_folder, block.template.file),
            ancor=block.ancor,
            title=block.title,
            introductory_text=block.introductory_text,
            button_text=block.button_text,
            products=[
                from_orm_to_product_type(type) for type in self.pr.get_product_types_for_catalog(block.id)
            ]
        )


def get_main_page_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return MainPageCatalogToBlockAssembler(product_repository)


class AdditionalCatalogBlockAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: AdditionalCatalogBlock, config: TemplateSettings = get_template_settings()) -> AdditionalCatalogBlockDTO:
        return AdditionalCatalogBlockDTO(
            name=block.name,
            template=os.path.join(config.blocks_templates_folder, block.template.file),
            ancor=block.ancor,
            button_text=block.button_text,
            add_annotation=block.add_annotation,
            add_button=block.add_button,
            products=[
                from_orm_to_product_type(type) for type in self.pr.get_proudct_types_for_additional_catalog(block.id)
            ]
        )


def get_additional_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return AdditionalCatalogBlockAssembler(product_repository)


class PromoCatalogAssembler:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.pr = product_repository

    def build_data(self, block: PromoCatalog, config: TemplateSettings = get_template_settings()) -> PromoCatalogDTO:
        return PromoCatalogDTO(
            name=block.name,
            template=os.path.join(config.blocks_templates_folder, block.template.file),
            ancor=block.ancor,
            title=block.title,
            products=[
                OfferDTO.process(offer) for offer in self.pr.get_offers()
            ]
        )


def get_promo_catalog_assembler(product_repository: ProductRepositoryInterface = get_product_repository()):
    return PromoCatalogAssembler(product_repository)


class CatalogAssembler:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        product_assembler: CatalogOfferAssembler
    ) -> None:
        self.pr = product_repository
        self.product_assembler = product_assembler

    def build_data(self, block: CatalogBlock, config: TemplateSettings = get_template_settings()) -> CatalogDTO:
        type = block.product_type

        print(hasattr(block, "user_is_authenticated"))
        if hasattr(block, "user_is_authenticated") and block.user_is_authenticated:
            products = self.pr.get_catalog_offers(type.slug)
        else:
            products = self.pr.get_catalog_offers(type.slug, private=False)

        products = [
            self.product_assembler.build_data(offer, type) for offer in products
        ]

        return CatalogDTO(
            name=block.name,
            template=os.path.join(config.blocks_templates_folder, block.template.file),
            ancor=block.ancor,
            button_text=block.button_text,
            button_ref=block.button_ref,
            title=block.title,
            introductory_text=block.introductory_text,
            add_category=block.add_category,
            exclusive_card=self.pr.get_exclusive_card() if block.add_exclusive else None,
            products=products
        )


def get_catalog_assembler(
    product_repository: ProductRepositoryInterface = get_product_repository(),
    product_assembler: CatalogOfferAssembler = get_catalog_offer_assembler()
) -> CatalogAssembler:
    return CatalogAssembler(product_repository, product_assembler)
