from typing import Protocol


class UserSessionRepositoryInterface(Protocol):
    def create_user_action(self, adress: str, text: str, session_unique_key: str) -> None:
        raise NotImplementedError
