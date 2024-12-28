from django.http import JsonResponse

from application.texts.errors import ErrorsMessages
from domain.email.exceptions import CantSendMailError


def email_exception_handler(exc):
    if isinstance(exc, CantSendMailError):
        return JsonResponse({"error": ErrorsMessages.something_went_wrong}, status=503)
