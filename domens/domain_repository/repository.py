from django.db.utils import OperationalError, ProgrammingError

from domens.domain_repository.repository_interface import DomainRepositoryInterface
from settings.models import Domain
from user.models.site import Site


class DomainRepository(DomainRepositoryInterface):
    @staticmethod
    def get_site(subdomain: str):
        try:
            return Site.objects.get(subdomain__iexact=subdomain)
        except Site.DoesNotExist:
            return None

    def get_domain_string(self):
        try:
            return Domain.objects.values_list("domain").filter(is_partners=False).first()
        except (OperationalError, ProgrammingError):
            return None

    def get_site_name(self) -> str | None:
        try:
            return Domain.objects.values_list("name").filter(is_partners=False).first()
        except (OperationalError, ProgrammingError):
            return None

    @classmethod
    def get_partners_domain_string(self) -> str:
        return Domain.objects.values_list("domain").filter(is_partners=True).first()[0]

    def get_partner_domain_model(self):
        return Domain.objects.filter(is_partners=True).first()

    @staticmethod
    def get_domain(domain: str):
        if Domain.objects.filter(domain=domain).exists():
            return Domain.objects.get(domain=domain)

    @staticmethod
    def get_domain_model_by_id(id: int):
        if Domain.objects.filter(id=id).exists():
            return Domain.objects.get(id=id)

        return None

    @staticmethod
    def get_domain_model():
        try:
            return Domain.objects.filter(is_partners=False).first()

        except (OperationalError, ProgrammingError):
            return None


def get_domain_repository() -> DomainRepository:
    return DomainRepository()
