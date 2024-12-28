from kombu.exceptions import OperationalError

from domain.email.exceptions import CantSendMailError
from infrastructure.email_services.tasks import send_email


class BaseEmailService:
    def send_email(self, *args, **kwargs) -> None:
        try:
            send_email.delay(*args, **kwargs)
        except OperationalError:
            raise CantSendMailError("cant send mail to user")
