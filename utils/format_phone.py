def get_raw_phone(phone: str) -> str:
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("(", "")
    phone = phone.replace(")", "")

    if phone[0] == "8":
        phone = "+7" + phone[1::]

    return phone
