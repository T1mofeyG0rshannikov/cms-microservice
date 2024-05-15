import re


def is_valid_phone(phone):
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("(", "")
    phone = phone.replace(")", "")

    pattern = re.compile(r"\+[7]\d{10}")
    if pattern.match(phone) and len(phone) == 12:
        return True

    return False
