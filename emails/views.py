from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from emails.email_service.email_service import get_email_service
from emails.email_service.email_service_interface import EmailServiceInterface
from emails.exceptions import CantSendMailError


class SendConfirmEmail(View):
    email_service: EmailServiceInterface = get_email_service()

    def get(self, request):
        user = request.user_from_header

        if user:
            try:
                self.email_service.send_mail_to_confirm_email(user)
            except CantSendMailError:
                return JsonResponse({"error": "Что-то пошло не так, повторите попытку чуть позже"}, status=503)

            return HttpResponse(status=200)

        return HttpResponse(status=401)
