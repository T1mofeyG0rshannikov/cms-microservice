from collections.abc import Iterable

from django.db.models import Q
from django.db.utils import IntegrityError

from application.texts.errors import SiteErrorsMessages
from domain.common.screen import FileInterface
from domain.user.sites.exceptions import SiteAdressExists
from domain.user.sites.site import SiteInterface
from domain.user.sites.site_repository import SiteRepositoryInterface
from infrastructure.persistence.models.user.site import Site


class SiteRepository(SiteRepositoryInterface):
    def get(self, subdomain: str = None, user_id: int = None, domain: str = None) -> SiteInterface:
        query = Q()
        if subdomain is not None:
            query &= Q(subdomain__iexact=subdomain)
        if user_id:
            query &= Q(user_id=user_id)
        if domain:
            query &= Q(domain__domain=domain)

        try:
            return Site.objects.get(query)
        except Site.DoesNotExist:
            return None

    def update_or_create(
        self, user_id: int, subdomain: str, name: str, owner: str = None, logo: FileInterface = None, **kwargs
    ) -> tuple[SiteInterface, bool]:
        try:
            site, created = Site.objects.update_or_create(
                user_id=user_id,
                defaults={
                    "subdomain": subdomain,
                    "name": name,
                    "owner": owner,
                    "contact_info": kwargs.get("contact_info"),
                    "font_id": kwargs.get("font_id"),
                    "font_size": kwargs.get("font_size"),
                    "domain_id": kwargs.get("domain_id"),
                    "logo_width": kwargs.get("logo_width"),
                    "user_id": user_id,
                },
            )

            if logo:
                site.logo = logo

            if kwargs.get("delete_logo") == "true":
                site.logo = None

            site.save()

            return site, created
        except IntegrityError:
            raise SiteAdressExists(SiteErrorsMessages.address_already_exists)

    def all(self) -> Iterable[SiteInterface]:
        return Site.objects.all()


def get_site_repository() -> SiteRepositoryInterface:
    return SiteRepository()
