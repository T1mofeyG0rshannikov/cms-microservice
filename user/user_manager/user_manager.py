from django.core.exceptions import MultipleObjectsReturned

from user.models import User
from user.user_manager.user_manager_interface import UserManagerInterface


class UserManager(UserManagerInterface):
    def get_user_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            last_user = User.objects.first()
            users_with_email_exclude_last = User.objects.exclude(created_at=last_user.created_at)
            users_with_email_exclude_last.update(email=None)

            return last_user

    def get_user_by_phone(self, phone: str) -> User | None:
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

    def create_user(self, data: dict) -> User:
        return User.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            phone=data.get("phone"),
        )

    def get_user_by_id(self, id: int) -> User | None:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None


def get_user_manager() -> UserManager:
    return UserManager()
