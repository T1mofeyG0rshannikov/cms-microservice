from django.core.exceptions import MultipleObjectsReturned

#from user.models import User
from user.user_manager.user_manager_interface import UserManagerInterface

from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model

#UserModel = get_user_model()

class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{"email": username})
    
    def create_user(self, username: str, phone: str, email: str, **extra_fields):
        return self.model.objects.create(
            username=username,
            email=email,
            phone=phone,
            **extra_fields
        )
        
    def create_superuser(self, username: str, phone: str, email: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, phone, email, **extra_fields)


def get_user_manager() -> UserManager:
    return UserManager()
