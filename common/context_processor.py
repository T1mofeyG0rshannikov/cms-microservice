from domens.get_domain import get_domain_string, get_partners_domain_string
from settings.get_settings import get_settings


def get_site_data(request):
    settings = get_settings(request.domain, request.subdomain)

    if request.domain == "localhost":
        domain = "localhost:8000"
    else:
        domain = get_domain_string()

    partner_domain = get_partners_domain_string()

    return {"settings": settings, "domain": domain, "partner_domain": partner_domain}
