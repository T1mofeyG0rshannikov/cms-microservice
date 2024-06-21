from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import MultipleObjectsReturned


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{"email": username})

    def get_user_by_id(self, id: int):
        try:
            return self.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get_user_by_email(self, email: str):
        try:
            return self.get(**{"email": email})
        except self.model.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            last_user = self.get_queryset().first()
            users_with_email_exclude_last = self.get_queryset().exclude(created_at=last_user.created_at)
            users_with_email_exclude_last.update(email=None)

            return last_user

    def get_user_by_phone(self, phone: str):
        try:
            return self.get(**{"phone": phone})
        except self.model.DoesNotExist:
            return None

    def create_user(self, username: str, phone: str, email: str, **extra_fields):
        return self.model.objects.create(username=username, email=email, phone=phone, **extra_fields)

    def create_superuser(self, username: str, phone: str, email: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, phone, email, **extra_fields)
