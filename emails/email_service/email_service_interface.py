from typing import Protocol

from user.user_interface import UserInterface


class EmailServiceInterface(Protocol):
    sender: str

    def send_mail_to_confirm_email(self, user: UserInterface) -> None:
        raise NotImplementedError()

    def send_mail_to_reset_password(self, user: UserInterface) -> None:
        raise NotImplementedError()
