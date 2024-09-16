from typing import Any

from web.account.models import UserSocialNetwork


class SocialsRepository:
    @staticmethod
    def delete_user_social(site_id: int) -> None:
        return UserSocialNetwork.objects.filter(site_id=site_id).delete()

    @staticmethod
    def user_social_exists(site_id: int, social_network_id: int) -> bool:
        return UserSocialNetwork.objects.filter(site_id=site_id, social_network_id=social_network_id).exists()

    @staticmethod
    def update_or_create_user_social(site_id: int, social_network_id: int, fields: dict[str, Any]) -> None:
        UserSocialNetwork.objects.update_or_create(
            social_network_id=social_network_id,
            site_id=site_id,
            defaults=fields,
        )


def get_socials_repository() -> SocialsRepository:
    return SocialsRepository()
