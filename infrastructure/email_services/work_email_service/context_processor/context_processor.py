from typing import Any

from .context_processor_interface import WorkEmailContextProcessorInterface


class WorkEmailContextProcessor(WorkEmailContextProcessorInterface):
    def try_login_in_admin(self, **kwargs) -> dict[str, Any]:
        context = {}
        context["ip"] = kwargs.get("ip")
        context["time"] = kwargs.get("time")
        context["login"] = kwargs.get("login")
        context["error"] = kwargs.get("error")

        return context

    def login_in_fake_admin(self, **kwargs) -> dict[str, Any]:
        context = {}
        context["ip"] = kwargs.get("ip")
        context["time"] = kwargs.get("time")
        context["login"] = kwargs.get("login")
        user = kwargs.get("user")
        if user and user.is_authenticated:
            user = user.email

        context["user"] = user

        return context

    def error_message(self, **kwargs) -> dict[str, Any]:
        context = {}
        context["client_ip"] = kwargs.get("client_ip")
        context["message"] = kwargs.get("message")
        context["path"] = kwargs.get("path")
        context["user"] = kwargs.get("user")

        return context

    def login_code(self, code: int, **kwargs) -> dict[str, Any]:
        context = {"code": code}

        return context


def get_work_email_context_processor() -> WorkEmailContextProcessorInterface:
    return WorkEmailContextProcessor()
