from django.db.utils import OperationalError, ProgrammingError

from domain.domains.domain import DomainInterface
from domain.domains.domain_repository import DomainRepositoryInterface
from infrastructure.persistence.models.settings import Domain


class DomainRepository(DomainRepositoryInterface):
    @classmethod
    def get_partners_domain_string(self) -> str:
        return Domain.objects.values_list("domain").filter(is_partners=True).first()[0]

    def get_domain_string(self) -> str:
        try:
            domain = Domain.objects.values_list("domain").filter(is_partners=False).first()
            if domain:
                return domain[0]

            return None
        except (OperationalError, ProgrammingError):
            return None

    def get_site_name(self) -> str | None:
        try:
            domain = Domain.objects.values_list("name").filter(is_partners=False).first()
            if domain:
                return domain[0]

            return None
        except (OperationalError, ProgrammingError):
            return None

    def get_partner_domain_model(self) -> DomainInterface:
        return Domain.objects.filter(is_partners=True).first()

    def get_domain(self, domain: str) -> DomainInterface:
        if Domain.objects.filter(domain=domain).exists():
            return Domain.objects.get(domain=domain)

    def get_domain_model(self) -> DomainInterface:
        try:
            return Domain.objects.filter(is_partners=False).first()

        except (OperationalError, ProgrammingError):
            return None


def get_domain_repository() -> DomainRepositoryInterface:
    return DomainRepository()
