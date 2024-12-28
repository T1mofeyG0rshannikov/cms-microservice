from typing import Any

from application.email_services.work_email_service.context_processor_interface import (
    WorkEmailContextProcessorInterface,
)
from domain.user.entities import UserInterface


class WorkEmailContextProcessor(WorkEmailContextProcessorInterface):
    def login_in_fake_admin(self, user: UserInterface, **kwargs) -> dict[str, Any]:
        if user:
            email = user.email

        return {
            "ip": kwargs.get("ip"),
            "time": kwargs.get("time"),
            "login": kwargs.get("username"),
            "password": kwargs.get("password"),
            "email": email,
        }

    def error_message(self, **kwargs) -> dict[str, Any]:
        return {
            "client_ip": kwargs.get("client_ip"),
            "message": kwargs.get("message"),
            "path": kwargs.get("path"),
            "user": kwargs.get("user"),
        }

    def login_code(self, code: int, **kwargs) -> dict[str, Any]:
        return {"code": code}


def get_work_email_context_processor() -> WorkEmailContextProcessorInterface:
    return WorkEmailContextProcessor()
