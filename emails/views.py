from django.http import HttpResponse

from emails.email_service.email_service import get_email_service
from emails.email_service.email_service_interface import EmailServiceInterface
from emails.email_service.link_generator.link_generator import get_link_generator
from user.auth.jwt_processor import get_jwt_processor
from django.views.generic import View
from domens.get_domain import get_domain_string


class SendConfirmEmail(View): 
    email_service: EmailServiceInterface = get_email_service(
        get_link_generator(
            get_jwt_processor(),
            get_domain_string()
        )
    )

    def get(self, request):
        user = request.user_from_header

        if user:
            self.email_service.send_mail_to_confirm_email(user)

        return HttpResponse(status=200)
