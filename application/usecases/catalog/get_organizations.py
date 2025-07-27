from dataclasses import asdict

from application.dto.product import OrganizationDTO
from domain.products.repository import (
    ProductFiltersInterface,
    ProductRepositoryInterface,
)
from infrastructure.persistence.db_filters.products import OrganizationFilter
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)


class GetOrganizations:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.r = product_repository

    def __call__(self, filters: ProductFiltersInterface) -> list[OrganizationDTO]:
        filters = OrganizationFilter(**asdict(filters))
        organizations = self.r.filter_organizations(filters)
        return [OrganizationDTO.process(organization) for organization in organizations]


def get_organizations_interactor(
    product_repositopry: ProductRepositoryInterface = get_product_repository(),
) -> GetOrganizations:
    return GetOrganizations(
        product_repository=product_repositopry,
    )
