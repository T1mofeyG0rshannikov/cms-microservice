from django.core.cache import cache
from django.db.models import Q
from django.db.utils import OperationalError, ProgrammingError

from domain.domains.domain import DomainInterface
from domain.domains.domain_repository import DomainRepositoryInterface
from infrastructure.persistence.models.settings import Domain, LandingDomain


class DomainRepository(DomainRepositoryInterface):
    @classmethod
    def get_partners_domain_string(self) -> str:
        domain_string = cache.get("partners_domain_string")
        if not domain_string:
            domain_string = Domain.objects.values_list("domain").get(is_partners=True)[0]
            cache.set("partners_domain_string", domain_string, timeout=60 * 15)

        return domain_string

    def get_domain_string(self) -> str:
        try:
            domain = cache.get("domain_string")
            if not domain:
                domain = Domain.objects.values_list("domain").filter(is_partners=False).first()[0]
                cache.set("domain_string", domain, timeout=60 * 15)

            return domain
        except (OperationalError, ProgrammingError, TypeError):
            return ""

    def get_site_name(self) -> str:
        try:
            domain = cache.get("site_name")
            if not domain:
                domain = Domain.objects.values_list("name").filter(is_partners=False).first()[0]
                cache.set("site_name", domain, timeout=60 * 15)

            return domain
        except (OperationalError, ProgrammingError):
            return ""

    def get_domain(self, domain: str | None = None, is_partners: bool | None = None) -> DomainInterface:
        query = Q()
        if domain:
            query &= Q(domain=domain)
        if is_partners is not None:
            query &= Q(is_partners=is_partners)

        return Domain.objects.filter(query).first()

    def landing_domain_exists(self, domain) -> bool:
        return LandingDomain.objects.filter(domain__iexact=domain).exists()


def get_domain_repository() -> DomainRepositoryInterface:
    return DomainRepository()
