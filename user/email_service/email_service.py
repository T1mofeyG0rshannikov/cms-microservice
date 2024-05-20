from django.conf import settings
from django.core.mail import send_mail

from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.email_service.email_service_interface import EmailServiceInterface
from user.models import User


class EmailService(EmailServiceInterface):
    def __init__(self, jwt_processor: JwtProcessorInterface):
        self.jwt_processor = jwt_processor

    def get_url_to_confirm_email(self, user_id: int) -> str:
        token_to_confirm_email = self.jwt_processor.create_confirm_email_token(user_id)
        return f"{settings.HOST}/user/confirm-email/{token_to_confirm_email}"

    def get_url_to_reset_password(self, user_id: int) -> str:
        token_to_reset_password = self.jwt_processor.create_set_password_token(user_id)
        return f"{settings.HOST}/user/password/{token_to_reset_password}"

    def send_mail_to_confirm_email(self, user: User) -> None:
        url = self.get_url_to_confirm_email(user.id)

        send_mail("Подтвердите почту", url, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def send_mail_to_reset_password(self, user: User) -> None:
        url = self.get_url_to_reset_password(user.id)

        send_mail(
            "Перейдите по ссылке для сброса пароля", url, settings.EMAIL_HOST_USER, [user.email], fail_silently=False
        )


def get_email_service(jwt_processor: JwtProcessorInterface) -> EmailService:
    return EmailService(jwt_processor)
