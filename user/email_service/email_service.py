from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.email_service.email_service_interface import EmailServiceInterface
from user.email_service.tasks import (
    send_mail_to_confirm_email,
    send_mail_to_reset_password,
)
from user.models import User
from domens.models import Domain


class EmailService(EmailServiceInterface):
    def __init__(self, jwt_processor: JwtProcessorInterface) -> None:
        self.jwt_processor = jwt_processor
        self.host = Domain.objects.filter(is_partners=False).first().domain

    def get_url_to_confirm_email(self, user_id: int) -> str:
        token_to_confirm_email = self.jwt_processor.create_confirm_email_token(user_id)
        return f"{self.host}/user/confirm-email/{token_to_confirm_email}"

    def get_url_to_reset_password(self, user_id: int) -> str:
        token_to_reset_password = self.jwt_processor.create_set_password_token(user_id)
        return f"{self.host}/user/password/{token_to_reset_password}"

    def send_mail_to_confirm_email(self, user: User) -> None:
        url = self.get_url_to_confirm_email(user.id)
        send_mail_to_confirm_email.delay(url, user.email)

    def send_mail_to_reset_password(self, user: User) -> None:
        url = self.get_url_to_reset_password(user.id)
        send_mail_to_reset_password.delay(url, user.email)


def get_email_service(jwt_processor: JwtProcessorInterface) -> EmailService:
    return EmailService(jwt_processor)
