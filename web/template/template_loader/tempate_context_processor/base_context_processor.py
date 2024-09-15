from django.http import HttpRequest


class BaseContextProcessor:
    @staticmethod
    def get_context(request: HttpRequest):
        context = {"request": request, "user": request.user}
        return context
