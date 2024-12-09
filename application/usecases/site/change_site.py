from domain.domains.domain_repository import DomainRepositoryInterface
from domain.domains.site import SiteInterface
from domain.domains.site_validator import SiteValidatorInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.user.site_validator import get_site_validator


class ChangeSite:
    def __init__(self, repository: DomainRepositoryInterface, validator: SiteValidatorInterface) -> None:
        self.repository = repository
        self.validator = validator

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
        name = self.validator.valid_name(name)
        subdomain = self.validator.valid_site(subdomain)
        logo = self.validator.valid_logo(logo)

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


def get_change_site_interactor(
    repository: DomainRepositoryInterface = get_domain_repository(),
    validator: SiteValidatorInterface = get_site_validator(),
) -> ChangeSite:
    return ChangeSite(repository, validator)
