from domens.models import Domain
from settings.get_settings import get_settings


def get_site_data(request):
    settings = get_settings(request.domain, request.subdomain)

    if request.domain == "localhost":
        domain = "localhost:8000"
    else:
        domain = Domain.objects.filter(is_partners=False).first().domain

    return {"settings": settings, "domain": domain}
