from typing import Any, Protocol


class SocialsRepositoryInterface(Protocol):
    @staticmethod
    def delete_user_social(site_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def user_social_exists(site_id: int, social_network_id: int) -> bool:
        raise NotImplementedError()

    @staticmethod
    def update_or_create_user_social(site_id: int, social_network_id: int, fields: dict[str, Any]) -> None:
        raise NotImplementedError()
