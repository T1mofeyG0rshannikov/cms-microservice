from typing import Protocol


class JwtProcessorInterface(Protocol):
    def create_set_password_token(self, user_id: int) -> dict:
        raise NotImplementedError()

    def create_access_token(self, username: str, user_id: int) -> dict:
        raise NotImplementedError()

    def validate_token(self, token: str) -> dict | bool:
        raise NotImplementedError()

    def create_confirm_email_token(self, user_id: int) -> str:
        raise NotImplementedError()
