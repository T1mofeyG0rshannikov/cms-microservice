import re
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


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


def is_valid_email(email: Any) -> bool:
    if not isinstance(email, str):
        return False

    email_validator = EmailValidator()
    try:
        email_validator(email)
        return True
    except ValidationError:
        return False
