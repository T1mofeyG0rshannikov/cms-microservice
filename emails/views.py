from django.http import HttpResponse

from emails.email_service.email_service import get_email_service
from emails.email_service.email_service_interface import EmailServiceInterface
from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.views.base_user_view import BaseUserView


class SendConfirmEmail(BaseUserView):
    def __init__(self):
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()
        self.email_service: EmailServiceInterface = get_email_service(self.jwt_processor)

    def get(self, request):
        user = request.user_from_header

        if user:
            self.email_service.send_mail_to_confirm_email(user)

        return HttpResponse(status=200)
