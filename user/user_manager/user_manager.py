from django.contrib.auth.models import BaseUserManager

from user.user_manager.user_manager_interface import UserManagerInterface
from user.validator.validator import get_user_validator
from user.validator.validator_interface import UserValidatorInterface


class UserManager(BaseUserManager, UserManagerInterface):
    validator: UserValidatorInterface = get_user_validator()

    def get_by_natural_key(self, username):
        if self.validator.is_valid_phone(username):
            return self.get_user_by_phone(username)

        elif self.validator.is_valid_email(username):
            return self.get_user_by_email(username)

        elif isinstance(username, str):
            return self.model.objects.filter(username=username).first()

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
