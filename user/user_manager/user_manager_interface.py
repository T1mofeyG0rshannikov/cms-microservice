from typing import Protocol

#from user.models import User

#from django.contrib.auth import get_user_model

#User = get_user_model()

class UserManagerInterface(Protocol):
    def get_user_by_email(self, email: str):# -> User | None:
        raise NotImplementedError()

    def get_user_by_phone(self, phone: str):# -> User | None:
        raise NotImplementedError()

    def create_user(self, data: dict):# -> User:
        raise NotImplementedError()

    def get_user_by_id(self, id: int):# -> User | None:
        raise NotImplementedError()
