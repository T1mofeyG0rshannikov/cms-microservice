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
