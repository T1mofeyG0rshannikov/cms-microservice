import re
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from domain.referrals.referral import ReferralInterface
from domain.user.exceptions import InvalidReferalLevel, InvalidSortedByField
from domain.user.validator import UserValidatorInterface


class UserValidator(UserValidatorInterface):
    @staticmethod
    def is_valid_phone(phone: Any) -> bool:
        if not isinstance(phone, str):
            return False

        phone = phone.replace(" ", "")
        phone = phone.replace("(", "")
        phone = phone.replace(")", "")
        phone = phone.replace("-", "")

        pattern1 = re.compile(r"\+[7]\d{10}")
        pattern2 = re.compile(r"8\d{10}")
        if (pattern1.match(phone) and len(phone) == 12) or (pattern2.match(phone) and len(phone) == 11):
            return True

        return False

    @staticmethod
    def is_valid_email(email: Any) -> bool:
        if not isinstance(email, str):
            return False

        email_validator = EmailValidator()
        try:
            email_validator(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def get_raw_phone(phone: str) -> str:
        phone = phone.replace(" ", "")
        phone = phone.replace("-", "")
        phone = phone.replace("(", "")
        phone = phone.replace(")", "")

        if phone[0] == "8":
            phone = "+7" + phone[1::]

        return phone

    @staticmethod
    def validate_sorted_by(sorted_by):
        if sorted_by[0] == "-":
            field = sorted_by[1::]
        else:
            field = sorted_by

        if field in ReferralInterface.__dataclass_fields__:
            return sorted_by

        raise InvalidSortedByField(f"User has no field '{sorted_by}'")

    @staticmethod
    def validate_referral_level(level) -> int:
        try:
            level = int(level)
        except:
            raise InvalidReferalLevel("the referral level can be only a number from 1 to 3 inclusive")

        if 0 < level < 4:
            return level

        raise InvalidReferalLevel("the referral level can be only a number from 1 to 3 inclusive")

    def validate_phone_or_email(self, phone_or_email: str) -> str | None:
        valid_as_email = self.is_valid_email(phone_or_email)
        valid_as_phone = self.is_valid_phone(self.get_raw_phone(phone_or_email))

        if not valid_as_email and not valid_as_phone:
            return None

        if valid_as_email:
            return phone_or_email
        else:
            return self.get_raw_phone(phone_or_email)


def get_user_validator() -> UserValidatorInterface:
    return UserValidator()
