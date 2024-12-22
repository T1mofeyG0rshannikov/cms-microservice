from django.contrib.auth.models import BaseUserManager

from domain.user.validator import UserValidatorInterface
from infrastructure.user.validator import get_user_validator


class UserManager(BaseUserManager):
    def __init__(self, validator: UserValidatorInterface = get_user_validator()):
        super().__init__()
        self.validator = validator

    def get_by_natural_key(self, username):
        if self.validator.is_valid_phone(username):
            return self.get(phone=username)

        elif self.validator.is_valid_email(username):
            return self.get(email=username)

        elif isinstance(username, str):
            return self.model.objects.filter(username=username).first()

        return super().get_by_natural_key(username)
