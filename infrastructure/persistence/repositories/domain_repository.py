from django.db.utils import IntegrityError, OperationalError, ProgrammingError

from domain.domains.domain import DomainInterface, SiteInterface
from domain.domains.exceptions import SiteAdressExists
from domain.domains.repository import DomainRepositoryInterface
from infrastructure.persistence.models.settings import Domain
from infrastructure.persistence.models.user.site import Site


class DomainRepository(DomainRepositoryInterface):
    def get_site(self, subdomain: str) -> SiteInterface:
        try:
            return Site.objects.get(subdomain__iexact=subdomain)
        except Site.DoesNotExist:
            return None

    def get_domain_string(self) -> str:
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

    def get_partner_domain_model(self) -> DomainInterface:
        return Domain.objects.filter(is_partners=True).first()

    def get_domain(self, domain: str) -> DomainInterface:
        if Domain.objects.filter(domain=domain).exists():
            return Domain.objects.get(domain=domain)

    def get_domain_model_by_id(self, id: int) -> DomainInterface:
        if Domain.objects.filter(id=id).exists():
            return Domain.objects.get(id=id)

        return None

    def get_domain_model(self) -> DomainInterface:
        try:
            return Domain.objects.filter(is_partners=False).first()

        except (OperationalError, ProgrammingError):
            return None

    def update_or_create_user_site(self, **kwargs) -> SiteInterface:
        fields = kwargs
        user_id = fields.get("user_id")

        try:
            site, _ = Site.objects.update_or_create(
                user_id=user_id,
                defaults={
                    "subdomain": fields["subdomain"],
                    "name": fields["name"],
                    "owner": fields["owner"],
                    "contact_info": fields["contact_info"],
                    "font_id": fields["font_id"],
                    "font_size": fields["font_size"],
                    "domain_id": fields["domain_id"],
                    "logo_width": fields["logo_width"],
                    "user_id": user_id,
                },
            )

            logo = fields.get("logo", None)
            if logo:
                site.logo = logo

            if fields.get("delete_logo") == "true":
                site.logo = None

            site.save()

            return site
        except IntegrityError:
            raise SiteAdressExists("Такой адрес уже существует")

    def site_adress_exists(self, site_id: int, site_url: str) -> bool:
        return Site.objects.get(id=site_id).subdomain != site_url and Site.objects.filter(subdomain=site_url).exists()

    def get_user_site(self, user_id: int) -> SiteInterface:
        return Site.objects.filter(user_id=user_id).first()

    def get_domain_sites(self, domain: str) -> list[SiteInterface]:
        return Site.objects.all() if domain == "localhost" else Site.objects.filter(domain__domain=domain)


def get_domain_repository() -> DomainRepositoryInterface:
    return DomainRepository()
