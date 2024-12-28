from domain.account.socials_repository import SocialsRepositoryInterface
from infrastructure.persistence.models.account import UserSocialNetwork


class SocialsRepository(SocialsRepositoryInterface):
    def delete(self, site_id: int) -> None:
        return UserSocialNetwork.objects.filter(site_id=site_id).delete()

    def update_or_create_user_social(self, site_id: int, social_network_id: int, adress: str | None = None) -> None:
        UserSocialNetwork.objects.update_or_create(
            social_network_id=social_network_id,
            site_id=site_id,
            defaults={"adress": adress},
        )


def get_socials_repository() -> SocialsRepositoryInterface:
    return SocialsRepository()
