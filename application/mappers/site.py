from domain.user.entities import SiteInterface
from infrastructure.persistence.models.user.site import Site


def from_orm_to_site(site: Site) -> SiteInterface:
    return SiteInterface(
        id=site.id,
        name=site.name,
        subdomain=site.subdomain,
        domain=site.domain,
        owner=site.owner,
        contact_info=site.contact_info,
        created_at=site.created_at,
        user=site.user,
        online_from=site.online_from,
        logo=site.logo,
        logo_width=site.logo_width,
        logo_width_mobile=site.logo_width_mobile,
        font=site.font,
        font_size=site.font_size,
        socials=site.socials.all()
    )