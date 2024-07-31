from domens.models import Domain


def get_domain_string() -> str:
    return Domain.objects.values_list("domain").filter(is_partners=False).first()[0]


def get_partners_domain_string() -> str:
    return Domain.objects.values_list("domain").filter(is_partners=True).first()[0]
