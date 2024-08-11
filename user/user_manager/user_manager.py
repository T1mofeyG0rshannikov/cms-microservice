from django.contrib.auth.models import BaseUserManager

from user.user_manager.user_manager_interface import UserManagerInterface
from utils.validators import is_valid_email, is_valid_phone


class UserManager(BaseUserManager, UserManagerInterface):
    def get_by_natural_key(self, username):
        if is_valid_phone(username):
            return self.get_user_by_phone(username)

        elif is_valid_email(username):
            return self.get_user_by_email(username)

        return super().get_by_natural_key(username)

    def get_user_by_id(self, id: int):
        try:
            return self.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get_user_by_email(self, email: str):
        try:
            if email:
                return self.get(**{"email": email})
            return None
        except self.model.DoesNotExist:
            return None

    def get_user_by_phone(self, phone: str):
        try:
            if phone:
                return self.get(**{"phone": phone})
            return None
        except self.model.DoesNotExist:
            return None

    def create_user(self, username: str, phone: str, email: str, **extra_fields):
        return self.model.objects.create(username=username, email=email, phone=phone, **extra_fields)

    def create_superuser(self, username: str, phone: str, email: str, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, phone, email, **extra_fields)
