from django.db.models import Q

from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralSerializer
from user.exceptions import InvalidSortedByField, UserIsNotReferral
from user.interfaces import UserInterface
from user.models import User
from user.validator.validator import get_user_validator
from user.validator.validator_interface import UserValidatorInterface
from utils.sort import sort_list_by_attr


class ReferralService(ReferralServiceInterface):
    total_referal_level: int = 3

    def __init__(self, validator: UserValidatorInterface):
        self.validator = validator

    def get_referral_level(self, referral, user):
        sponsor = referral.sponsor
        for i in range(self.total_referal_level):
            if sponsor.id == user.id:
                return i + 1

            sponsor = sponsor.sponsor

        raise UserIsNotReferral(f"user '{user.full_name}' is not '{referral.full_name}'`s sponsor")

    def get_referral(self, user_id: int, user: UserInterface):
        if not User.objects.filter(id=user_id).exists():
            raise User.DoesNotExist

        referral = User.objects.get(id=user_id)
        referral.level = self.get_referral_level(referral, user)

        return ReferralSerializer(referral).data

    def get_referrals_count(self, level, referral):
        count = 0
        for i in range(level):
            field = "sponsor__" * i + "sponsor_id"
            count += User.objects.filter(Q(**{field: referral.id})).count()

        return count

    def set_referrals_count(self, referrals):
        for referral in referrals:
            referral.first_level_referrals = self.get_referrals_count(1, referral)
            referral.referrals = referral.first_level_referrals + sum(
                [self.get_referrals_count(i, referral) for i in range(self.total_referal_level)]
            )

        return referrals

    def get_referrals_by_level(self, sponsor, level):
        query = "sponsor__" * (level - 1) + "sponsor_id"
        return User.objects.filter(Q(**{query: sponsor.id}))

    def set_referral_level(self, referrals: list[User], level: int) -> list[User]:
        for referral in referrals:
            referral.level = level

        return referrals

    def get_referrals(self, user: User, level=None, sorted_by=None) -> list[User]:
        if level:
            level = self.validator.validate_referral_level(level)
        if sorted_by:
            sorted_by = self.validator.validate_sorted_by(sorted_by)

        if not level:
            referrals = []
            for i in range(self.total_referal_level):
                referrals.extend(self.set_referral_level(self.get_referrals_by_level(user, i + 1), i + 1))

        else:
            query = "sponsor__" * (level - 1) + "sponsor_id"
            referrals = User.objects.filter(Q(**{query: user.id}))

            self.set_referral_level(referrals, level)

        referrals = self.set_referrals_count(referrals)

        if sorted_by:
            try:
                referrals = sort_list_by_attr(referrals, sorted_by)
            except ValueError:
                raise InvalidSortedByField(f"User has no field '{sorted_by}'")

        return referrals


def get_referral_service() -> ReferralService:
    return ReferralService(get_user_validator())
