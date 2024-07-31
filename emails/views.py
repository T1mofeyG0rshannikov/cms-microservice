from django.http import HttpResponse
from django.views.generic import View

from emails.email_service.email_service import get_email_service
from emails.email_service.email_service_interface import EmailServiceInterface


class SendConfirmEmail(View):
    email_service: EmailServiceInterface = get_email_service()

    def get(self, request):
        user = request.user_from_header

        if user:
            self.email_service.send_mail_to_confirm_email(user)

        return HttpResponse(status=200)
