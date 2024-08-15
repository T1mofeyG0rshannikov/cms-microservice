from typing import Any, Protocol


class UserValidatorInterface(Protocol):
    @staticmethod
    def is_valid_phone(phone: Any) -> bool:
        raise NotImplementedError()

    @staticmethod
    def is_valid_email(email: Any) -> bool:
        raise NotImplementedError()

    @staticmethod
    def get_raw_phone(phone: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def validate_sorted_by(sorted_by: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def validate_referral_level(level) -> int:
        raise NotImplementedError()

    def validate_phome_or_email(self, phone_or_email: str) -> str | None:
        raise NotImplementedError()
