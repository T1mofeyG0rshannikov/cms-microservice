from typing import Any, Protocol

from domain.user.user import UserInterface


class UserRepositoryInterface(Protocol):
    def get_user_by_id(self, id: int) -> UserInterface | None:
        raise NotImplementedError
    
    def get_supersponsor(self) -> UserInterface:
        raise NotImplementedError

    def get_user_by_phone(self, phone: str) -> UserInterface | None:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> UserInterface | None:
        raise NotImplementedError
    
    def verify_password(self, user_id: int, password: str) -> bool:
        raise NotImplementedError
    
    def create_user(self, fields: dict[str, Any]) -> UserInterface | None:
        raise NotImplementedError
    
    def set_password(self, user_id: int, password: str) -> UserInterface:
        raise NotImplementedError
