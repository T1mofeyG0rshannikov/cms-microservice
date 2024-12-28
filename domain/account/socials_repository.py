from typing import Protocol


class SocialsRepositoryInterface(Protocol):
    def delete(self, site_id: int) -> None:
        raise NotImplementedError

    def update_or_create_user_social(self, site_id: int, social_network_id: int, adress: str | None = None) -> None:
        raise NotImplementedError
