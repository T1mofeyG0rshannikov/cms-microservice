from typing import Protocol


class LinkGeneratorInterface(Protocol):
    def get_url_to_confirm_email(self, user_id: int) -> str:
        raise NotImplementedError

    def get_url_to_confirm_new_email(self, user_id: int) -> str:
        raise NotImplementedError

    def get_url_to_reset_password(self, user_id: int) -> str:
        raise NotImplementedError
