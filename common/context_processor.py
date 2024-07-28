from domens.models import Domain
from settings.get_settings import get_settings


def get_site_data(request):
    settings = get_settings(request.domain, request.subdomain)

    if request.domain == "localhost":
        domain = "localhost:8000"
    else:
        domain = Domain.objects.filter(is_partners=False).values("domain").first()["domain"]

    partner_domain = Domain.objects.filter(is_partners=True).values("domain").first()["domain"]

    return {"settings": settings, "domain": domain, "partner_domain": partner_domain}
