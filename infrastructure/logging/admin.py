from typing import Any

from django.http import HttpRequest

from domain.email.exceptions import CantSendMailError
from domain.email.repository import SystemRepositoryInterface
from domain.logging.admin import AdminLogRepositoryInterface
from infrastructure.email_service.email_service_interface import EmailServiceInterface


class AdminLoginLogger:
    def __init__(
        self,
        repository: AdminLogRepositoryInterface,
        email_service: EmailServiceInterface,
        system_repository: SystemRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.email_service = email_service
        self.system_repository = system_repository

    @staticmethod
    def get_client_ip(request: HttpRequest):
        x_forwarded_for = request.META.get("HTTP_X_REAL_IP")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def error(self, request: HttpRequest, fields: dict[str, Any], error: str) -> None:
        ip_address = self.get_client_ip(request)
        print(ip_address)
        self.repository.create_logg(ip_address, **fields)

        emails = self.system_repository.get_system_emails()

        self.email_service.send_error_admin_login_message(emails, **fields, error=error)

    def success(self, request: HttpRequest, fields: dict[str, Any]) -> None:
        ip_address = self.get_client_ip(request)
        print(ip_address)
        self.repository.create_logg(ip_address, **fields)

        emails = self.system_repository.get_system_emails()

        self.email_service.send_success_admin_login_message(emails, **fields)

    def fake_admin_panel(self, request: HttpRequest, fields: dict[str, Any]) -> None:
        ip_address = self.get_client_ip(request)
        print(ip_address)
        self.repository.create_logg(ip_address, **fields)

        emails = self.system_repository.get_system_emails()

        self.email_service.send_fake_admin_login_message(emails, **fields)
