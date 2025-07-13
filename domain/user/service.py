from typing import Protocol


class UserServiceInterface(Protocol):
    def get_user(self, login: str, password: str):
        raise NotImplementedError
