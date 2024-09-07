from django.db.models import Q

from user.models.user import User
from user.user_repository.repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
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
        return User.objects.filter(Q(**{query: sponsor.id}))


def get_user_repository() -> UserRepository:
    return UserRepository()
