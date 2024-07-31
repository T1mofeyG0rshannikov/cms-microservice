from typing import Protocol


class EmailServiceInterface(Protocol):
    sender: str

    def send_mail_to_confirm_email(self, user) -> None:
        raise NotImplementedError()

    def send_mail_to_reset_password(self, user) -> None:
        raise NotImplementedError()
