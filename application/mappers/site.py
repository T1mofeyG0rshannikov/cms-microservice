from infrastructure.persistence.models.account import UserSocialNetwork
from domain.user.entities import SiteInterface, UserSocialNetworkInterface
from infrastructure.persistence.models.user.site import Site


def from_orm_to_user_social(social: UserSocialNetwork) -> UserSocialNetworkInterface:
    return UserSocialNetworkInterface(
        adress=social.adress,
        social_network=social.social_network.name
    )

def from_orm_to_site(site: Site) -> SiteInterface:
    return SiteInterface(
        id=site.id,
        name=site.name,
        subdomain=site.subdomain,
        domain=str(site.domain),
        owner=site.owner,
        contact_info=site.contact_info,
        created_at=site.created_at,
        user_id=site.user_id,
        online_from=site.online_from,
        logo=site.logo.url if site.logo else None,
        logo_width=site.logo_width,
        logo_width_mobile=site.logo_width_mobile,
        font=site.font.name,
        font_size=site.font_size,
        socials=[
            from_orm_to_user_social(social) for social in site.socials.all()
        ]
    )
