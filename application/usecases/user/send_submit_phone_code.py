from random import randrange

from application.sms_service_interface import SMSServiceInterface
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.email.repository import SystemRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)
from infrastructure.sms_service.sms_service import get_sms_service


class SendConfirmPhoneCode:
    def __init__(
        self,
        system_repository: SystemRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        sms_service: SMSServiceInterface,
    ) -> None:
        self.system_repository = system_repository
        self.domain_repository = domain_repository
        self.sms_service = sms_service

    def __call__(self, user_id: int, phone: str) -> None:
        code = self.generate_code()
        self.system_repository.update_or_create_confirm_phone_code(user_id=user_id, code=code, phone=phone)

        site_name = self.domain_repository.get_domain_string()

        self.sms_service.confirm_phone_code(site_name, phone, code)

    @staticmethod
    def generate_code(length: int = 6) -> str:
        code = str(randrange(0, 10**length))
        code = "0" * (length - len(code)) + code
        return code


def get_confirm_phone_interactor(
    system_repository: SystemRepositoryInterface = get_system_repository(),
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    sms_service: SMSServiceInterface = get_sms_service(),
) -> SendConfirmPhoneCode:
    return SendConfirmPhoneCode(
        system_repository=system_repository, domain_repository=domain_repository, sms_service=sms_service
    )
