from domain.account.socials_repository import SocialsRepositoryInterface
from domain.user.exceptions import SocialChannelAlreadyExists
from infrastructure.persistence.repositories.socials_repositry import (
    get_socials_repository,
)


class ChangeSocials:
    def __init__(self, repository: SocialsRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, site_id: int, user_social_networks: dict[str, str]):
        if len({social_network["social"] for social_network in user_social_networks}) < len(user_social_networks):
            raise SocialChannelAlreadyExists("Вы можете указать только один канал для каждой соц. сети")

        self.repository.delete(site_id)

        if user_social_networks:
            for user_social_network in user_social_networks:
                self.repository.update_or_create_user_social(
                    site_id=site_id,
                    social_network_id=user_social_network["social"],
                    adress=user_social_network["adress"],
                )


def get_change_socials_interactor(repository: SocialsRepositoryInterface = get_socials_repository()) -> ChangeSocials:
    return ChangeSocials(repository)
