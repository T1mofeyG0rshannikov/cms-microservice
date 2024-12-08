from typing import Protocol


class WorkEmailServiceInterface(Protocol):
    sender: str

    def send_success_admin_login_message(self, emails: list[str], **kwargs) -> None:
        raise NotImplementedError

    def send_error_admin_login_message(self, emails: list[str], **kwargs) -> None:
        raise NotImplementedError

    def send_fake_admin_login_message(self, emails: list[str], **kwargs) -> None:
        raise NotImplementedError

    def send_error_emails(self, emails: list[str], **kwargs) -> None:
        raise NotImplementedError

    def send_code_to_login_in_admin(self, email: str, code: int) -> None:
        raise NotImplementedError

    def send_feedback_email(self, **kwargs) -> None:
        raise NotImplementedError
