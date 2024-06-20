from django.core.exceptions import MultipleObjectsReturned

from user.models import User
from user.user_manager.user_manager_interface import UserManagerInterface

from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model

#UserModel = get_user_model()
        

class UserService:
    def get_user_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            last_user = User.objects.first()
            users_with_email_exclude_last = User.objects.exclude(created_at=last_user.created_at)
            users_with_email_exclude_last.update(email=None)

            return last_user

    def get_user_by_phone(self, phone: str):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None


    def create_user(self, username: str, phone: str, email: str, **extra_fields):
        return User.objects.create(
            username=username,
            email=email,
            phone=phone,
            **extra_fields
        )
        
    def create_superuser(self, username: str, phone: str, email: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, phone, email, **extra_fields)
        
    def get_user_by_id(self, id: int):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None


def get_user_manager() -> UserService:
    return UserService()
