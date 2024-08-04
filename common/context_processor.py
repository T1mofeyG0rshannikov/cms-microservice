from domens.domain_service.domain_service import DomainService
from settings.get_settings import get_settings


def get_site_data(request):
    settings = get_settings(request)

    if request.domain == "localhost":
        domain = "localhost:8000"
    else:
        domain = DomainService.get_domain_string()

    partner_domain = DomainService.get_partners_domain_string()

    return {"settings": settings, "domain": domain, "partner_domain": partner_domain}
