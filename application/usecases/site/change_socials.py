from domain.user.exceptions import SocialChannelAlreadyExists


class ChangeSocials:
    def __init__(self, repository):
        self.repository = repository

    def __call__(self, site_id: int, user_social_networks):
        if len({social_network["social"] for social_network in user_social_networks}) < len(user_social_networks):
            raise SocialChannelAlreadyExists("Вы можете указать только один канал для каждой соц. сети")

        self.repository.delete_user_social(site_id)

        if user_social_networks:
            for user_social_network in user_social_networks:
                self.repository.update_or_create_user_social(
                    site_id=site_id,
                    social_network_id=user_social_network["social"],
                    fields={"adress": user_social_network["adress"]},
                )
