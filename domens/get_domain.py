from django.db.utils import OperationalError

from domens.models import Domain


def get_domain_string() -> str | None:
    try:
        domain = Domain.objects.values_list("domain").filter(is_partners=False).first()
        if domain is None:
            return None

        return domain[0]

    except OperationalError:
        return None


def get_partners_domain_string() -> str:
    return Domain.objects.values_list("domain").filter(is_partners=True).first()[0]
