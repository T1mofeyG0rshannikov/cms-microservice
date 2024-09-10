from django.db import transaction
from django.db.models import Count, Q

from user.models.user import User
from user.user_repository.repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    @staticmethod
    def get_user_by_phone(phone: str):
        return User.objects.get_user_by_phone(phone)

    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.get_user_by_email(email)

    @staticmethod
    def get_supersponsor():
        return User.objects.filter(supersponsor=True).first()

    @staticmethod
    def get_user_by_id(id: int) -> User | None:
        return User.objects.get_user_by_id(id)

    @staticmethod
    def get_referrals_count(level: int, referral_id: int) -> int:
        count = 0
        for i in range(level):
            field = "sponsor__" * i + "sponsor_id"
            count += User.objects.filter(Q(**{field: referral_id})).count()

        return count

    @staticmethod
    def get_referrals_by_level(sponsor: User, level: int):
        query = "sponsor__" * (level - 1) + "sponsor_id"
        return User.objects.annotate(first_level_referrals=Count("sponsors")).filter(Q(**{query: sponsor.id}))

    @staticmethod
    def create_user(**kwargs) -> User:
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


def get_user_repository() -> UserRepository:
    return UserRepository()
