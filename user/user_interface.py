from dataclasses import dataclass


@dataclass
class UserInterface:
    id: int
    username: str
    second_name: str

    phone: str
    phone_is_confirmed: bool

    email: str
    new_email: str
    email_is_confirmed: str
