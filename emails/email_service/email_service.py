from domens.get_domain import get_domain_string
from emails.email_service.email_service_interface import EmailServiceInterface
from emails.email_service.tasks import (
    send_mail_to_confirm_email,
    send_mail_to_reset_password,
)
from user.auth.jwt_processor_interface import JwtProcessorInterface


class EmailService(EmailServiceInterface):
    def __init__(self, jwt_processor: JwtProcessorInterface) -> None:
        self.jwt_processor = jwt_processor
        self.host = get_domain_string()

    def get_url_to_confirm_email(self, user_id: int) -> str:
        token_to_confirm_email = self.jwt_processor.create_confirm_email_token(user_id)
        return f"http://{self.host}/user/confirm-email/{token_to_confirm_email}"

    def get_url_to_reset_password(self, user_id: int) -> str:
        token_to_reset_password = self.jwt_processor.create_set_password_token(user_id)
        return f"{self.host}/user/password/{token_to_reset_password}"

    def send_mail_to_confirm_email(self, user) -> None:
        url = self.get_url_to_confirm_email(user.id)
        send_mail_to_confirm_email.delay(url, user.email)

    def send_mail_to_reset_password(self, user) -> None:
        url = self.get_url_to_reset_password(user.id)
        send_mail_to_reset_password.delay(url, user.email)


def get_email_service(jwt_processor: JwtProcessorInterface) -> EmailService:
    return EmailService(jwt_processor)
