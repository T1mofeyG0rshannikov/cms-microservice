from typing import Protocol

from domain.user.interfaces import UserInterface


class EmailServiceInterface(Protocol):
    sender: str

    @staticmethod
    def send_email(*args, **kwargs) -> None:
        raise NotImplementedError()

    def send_mail_to_confirm_email(self, user: UserInterface) -> None:
        raise NotImplementedError()

    def send_mail_to_reset_password(self, user: UserInterface) -> None:
        raise NotImplementedError()
