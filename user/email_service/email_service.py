from django.conf import settings
from django.core.mail import send_mail

from user.auth.jwt_processor import get_jwt_processor
from user.models import User


class EmailService:
    def __init__(self):
        self.jwt_processor = get_jwt_processor()

    def send_main_to_confirm_email(self, user: User) -> None:
        token_to_confirm_email = self.jwt_processor.create_confirm_email_token(user.id)

        url = f"{settings.HOST}/user/confirm-email/{token_to_confirm_email}"

        send_mail("Подтвердите почту", url, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def get_email_service() -> EmailService:
    return EmailService()
