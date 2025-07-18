from infrastructure.persistence.models.catalog.product_type import ProductType
from domain.products.product import ProductTypeInterface


def from_orm_to_product_type(type: ProductType):
    return ProductTypeInterface(
        status=type.status,
        name=type.name,
        slug=type.slug,
        title=type.title,
        image=type.image.url,
        description=type.description,
        profit=type.profit,
    )