from account.models import UserMessanger
from django.db import transaction
from django.db.models import Count, Q
from user.interfaces import UserInterface
from user.models.user import User
from user.user_repository.repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    @staticmethod
    def get_user_by_phone(phone: str) -> UserInterface:
        return User.objects.get_user_by_phone(phone)

    @staticmethod
    def get_user_by_email(email: str) -> UserInterface:
        return User.objects.get_user_by_email(email)

    @staticmethod
    def get_supersponsor() -> UserInterface:
        return User.objects.filter(supersponsor=True).first()

    @staticmethod
    def get_user_by_id(id: int) -> UserInterface | None:
        return User.objects.get_user_by_id(id)

    @staticmethod
    def get_referrals_count(level: int, referral_id: int) -> int:
        count = 0
        for i in range(level):
            field = "sponsor__" * i + "sponsor_id"
            count += User.objects.filter(Q(**{field: referral_id})).count()

        return count

    @staticmethod
    def get_referrals_by_level(sponsor_id: int, level: int):
        query = "sponsor__" * (level - 1) + "sponsor_id"
        return User.objects.annotate(first_level_referrals=Count("sponsors")).filter(Q(**{query: sponsor_id}))

    @staticmethod
    def create_user(**kwargs) -> UserInterface:
        email = kwargs.get("email")
        phone = kwargs.get("phone")

        try:
            with transaction.atomic():
                User.objects.filter(email=email).update(email=None)
                User.objects.filter(phone=phone).update(phone=None)

                user = User.objects.create_user(**kwargs)

                return user
        except Exception as e:
            print(e)
            return None

    def verify_password(self, user_id: int, password: str) -> bool:
        return self.get_user_by_id(user_id).verify_password(password)

    @staticmethod
    def update_or_create_user_messanger(**kwargs) -> None:
        UserMessanger.objects.update_or_create(user_id=kwargs.get("user_id"), defaults=kwargs)

    def update_user(self, **kwargs) -> None:
        user = self.get_user_by_id(kwargs.get("id"))

        user.username = kwargs.get("username")
        user.second_name = kwargs.get("second_name")
        user.phone = kwargs.get("phone")

        if profile_picture := kwargs.get("profile_picture"):
            user.profile_picture = profile_picture

        user.save()

    def change_user_email(self, user_id: int, email: str) -> None:
        user = self.get_user_by_id(user_id)
        user.change_email(email)
        user.save()

    def set_password(self, user_id: int, new_password: str) -> UserInterface:
        user = self.get_user_by_id(user_id)
        user.set_password(new_password)
        user.save()

        return user


def get_user_repository() -> UserRepository:
    return UserRepository()
