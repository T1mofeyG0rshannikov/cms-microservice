from dataclasses import asdict

from application.dto.product import ProductDTO
from application.dto_builders.product import ProductAssembler, get_product_dto_builder
from domain.products.repository import (
    ProductFiltersInterface,
    ProductRepositoryInterface,
)
from infrastructure.persistence.db_filters.products import ProductFilters
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class GetProduct:
    def __init__(self, product_repository: ProductRepositoryInterface, dto_builder: ProductAssembler) -> None:
        self.r = product_repository
        self.builder = dto_builder

    def __call__(self, product_id: int) -> ProductDTO:
        product = self.r.get(product_id)
        return self.builder.process(product)


class GetProducts:
    def __init__(self, product_repository: ProductRepositoryInterface, dto_builder: ProductAssembler) -> None:
        self.r = product_repository
        self.builder = dto_builder

    def __call__(self, filters: ProductFiltersInterface) -> list[ProductDTO]:
        filters = ProductFilters(**asdict(filters))
        products = self.r.filter(filters)
        return [self.builder.process(product) for product in products]


def get_products_interactor(
    product_repositopry: ProductRepositoryInterface = get_product_repository(),
    dto_builder: ProductAssembler = get_product_dto_builder(),
) -> GetProducts:
    return GetProducts(product_repository=product_repositopry, dto_builder=dto_builder)


def get_product_interactor(
    product_repositopry: ProductRepositoryInterface = get_product_repository(),
    dto_builder: ProductAssembler = get_product_dto_builder(),
) -> GetProduct:
    return GetProduct(product_repository=product_repositopry, dto_builder=dto_builder)
