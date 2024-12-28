from django.db import transaction
from django.db.models import Q, QuerySet

from domain.common.screen import FileInterface
from domain.user.entities import UserInterface
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.models.account import UserMessanger
from infrastructure.persistence.models.user.user import User


class UserRepository(UserRepositoryInterface):
    def __filter_query(
        self,
        phone: str | None = None,
        email: str | None = None,
        id: int | None = None,
        supersponsor: bool | None = None,
    ) -> QuerySet[User]:
        query = Q()
        if phone:
            query &= Q(phone=phone)
        if email:
            query &= Q(email=email)
        if id:
            query &= Q(id=id)
        if supersponsor:
            query &= Q(supersponsor=supersponsor)

        return User.objects.filter(query)

    def get(
        self,
        phone: str | None = None,
        email: str | None = None,
        id: int | None = None,
        supersponsor: bool | None = None,
    ) -> UserInterface:
        return self.__filter_query(phone=phone, email=email, id=id, supersponsor=supersponsor).first()

    def create(self, email: str, phone: str, **kwargs) -> UserInterface | None:
        try:
            with transaction.atomic():
                User.objects.filter(email=email).update(email=None)
                User.objects.filter(phone=phone).update(phone=None)

                user = User.objects.create(email=email, phone=phone, **kwargs)

                return user
        except Exception as e:
            print(e)
            return None

    def verify_password(self, user_id: int, password: str) -> bool:
        return self.__filter_query(id=user_id).first().verify_password(password)

    def update_or_create_messanger(self, user_id: int, messanger_id: int, adress: str) -> None:
        UserMessanger.objects.update_or_create(
            user_id=user_id, defaults={"adress": adress, "messanger_id": messanger_id}
        )

    def update(
        self,
        id: int,
        username: str,
        second_name: str,
        phone: str,
        phone_is_confirmed: bool,
        profile_picture: FileInterface | None = None,
    ) -> None:
        user = self.__filter_query(id=id).first()

        user.username = username
        user.second_name = second_name
        user.phone = phone
        user.phone_is_confirmed = phone_is_confirmed

        if profile_picture:
            user.profile_picture = profile_picture

        user.save()

    def change_email(self, user_id: int, email: str) -> None:
        user = self.__filter_query(id=user_id).first()
        user.change_email(email)

    def set_password(self, user_id: int, new_password: str) -> UserInterface:
        user = self.get(id=user_id)
        user.set_password(new_password)

        return user

    def confirm_phone(self, user_id: int) -> None:
        User.objects.get(id=user_id).confirm_phone()


def get_user_repository() -> UserRepositoryInterface:
    return UserRepository()
