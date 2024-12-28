from typing import Protocol


class SMSServiceInterface(Protocol):
    def confirm_phone_code(self, site_name: str, phone: int, code: str) -> None:
        raise NotImplementedError
