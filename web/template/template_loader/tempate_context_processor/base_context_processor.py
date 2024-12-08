from typing import Any

from django.http import HttpRequest


class BaseContextProcessor:
    @staticmethod
    def get_context(request: HttpRequest) -> dict[str, Any]:
        return {"request": request, "user": request.user}
