from typing import Any

from django.http import HttpRequest


class BaseContextProcessor:
    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        return {"request": request, "user": request.user}
