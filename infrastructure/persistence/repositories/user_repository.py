from django.db import transaction
from django.db.models import Q

from domain.common.screen import FileInterface
from domain.user.repository import UserRepositoryInterface
from domain.user.user import UserInterface
from infrastructure.persistence.models.account import UserMessanger
from infrastructure.persistence.models.user.user import User


class UserRepository(UserRepositoryInterface):
    def get(self, phone: str = None, email: str = None, id: int = None, supersponsor: bool = None) -> UserInterface:
        query = Q()
        if phone:
            query &= Q(phone=phone)
        if email:
            query &= Q(email=email)
        if id:
            query &= Q(id=id)
        if supersponsor:
            query &= Q(supersponsor=supersponsor)

        try:
            return User.objects.filter(query).first()
        except User.DoesNotExist:
            return None

    def create(self, email: str, phone: str, **kwargs) -> UserInterface:
        try:
            with transaction.atomic():
                User.objects.filter(email=email).update(email=None)
                User.objects.filter(phone=phone).update(phone=None)

                user = User.objects.create(email=email, phone=phone, **kwargs)

                return user
        except Exception as e:
            print(e, "error_while create user")
            return None

    def verify_password(self, user_id: int, password: str) -> bool:
        return self.get(id=user_id).verify_password(password)

    def update_or_create_messanger(self, user_id: int, **kwargs) -> None:
        UserMessanger.objects.update_or_create(user_id=user_id, defaults=kwargs)

    def update(
        self, id: int, username: str, second_name: str, phone: str, profile_picture: FileInterface = None
    ) -> None:
        user = self.get(id=id)

        user.username = username
        user.second_name = second_name
        user.phone = phone

        if profile_picture:
            user.profile_picture = profile_picture

        user.save()

    def change_email(self, user_id: int, email: str) -> None:
        user = self.get(id=user_id)
        user.change_email(email)

    def set_password(self, user_id: int, new_password: str) -> UserInterface:
        user = self.get(id=user_id)
        user.set_password(new_password)

        return user

    def confirm_phone(self, user_id: int) -> None:
        User.objects.get(id=user_id).confirm_phone()


def get_user_repository() -> UserRepositoryInterface:
    return UserRepository()
