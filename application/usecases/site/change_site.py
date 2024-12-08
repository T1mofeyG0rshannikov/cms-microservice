from domain.domains.domain_repository import DomainRepositoryInterface
from domain.domains.site import SiteInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)


class ChangeSite:
    def __init__(self, repository: DomainRepositoryInterface) -> None:
        self.repository = repository

    def __call__(
        self,
        user_id: int,
        domain_id: int,
        subdomain: str,
        font_id: int,
        logo_size: int,
        name: str,
        owner: str,
        logo: str,
        delete_logo: str,
        contact_info: str,
        font_size: int,
    ) -> tuple[SiteInterface, bool]:
        if delete_logo == "true":
            logo = None

        return self.repository.update_or_create_user_site(
            user_id=user_id,
            domain_id=domain_id,
            subdomain=subdomain,
            logo_width=int(260 * (logo_size / 100)),
            font_id=font_id,
            name=name,
            owner=owner,
            contact_info=contact_info,
            font_size=font_size,
            logo=logo,
        )


def get_change_site_interactor(repository: DomainRepositoryInterface = get_domain_repository()) -> ChangeSite:
    return ChangeSite(repository)
