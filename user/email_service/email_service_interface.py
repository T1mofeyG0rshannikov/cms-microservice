from typing import Protocol

from user.models import User


class EmailServiceInterface(Protocol):
    def get_url_to_confirm_email(self, user_id: int) -> str:
        raise NotImplementedError()

    def get_url_to_reset_password(self, user_id: int) -> str:
        raise NotImplementedError()

    def send_mail_to_confirm_email(self, user: User) -> None:
        raise NotImplementedError()

    def send_mail_to_reset_password(self, user: User) -> None:
        raise NotImplementedError()
