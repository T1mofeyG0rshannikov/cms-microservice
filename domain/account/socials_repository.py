from typing import Protocol


class SocialsRepositoryInterface(Protocol):
    def delete_user_social(self, site_id: int) -> None:
        raise NotImplementedError

    def user_social_exists(self, site_id: int, social_network_id: int) -> bool:
        raise NotImplementedError

    def update_or_create_user_social(self, site_id: int, social_network_id: int, **kwargs) -> None:
        raise NotImplementedError
