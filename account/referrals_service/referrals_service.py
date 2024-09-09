from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralSerializer
from infrastructure.persistence.repositories.user_repository import get_user_repository
from user.exceptions import InvalidSortedByField, UserDoesNotExist, UserIsNotReferral
from user.interfaces import ReferralInterface, UserInterface
from user.user_repository.repository_interface import UserRepositoryInterface
from user.validator.validator import get_user_validator
from user.validator.validator_interface import UserValidatorInterface
from utils.sort import sort_list_by_attr


class ReferralService(ReferralServiceInterface):
    total_referal_level: int = 3

    def __init__(self, validator: UserValidatorInterface, repository: UserRepositoryInterface):
        self.validator = validator
        self.repository = repository

    def get_referral_level(self, referral, user):
        sponsor = referral.sponsor
        for i in range(self.total_referal_level):
            if sponsor.id == user.id:
                return i + 1

            sponsor = sponsor.sponsor

        raise UserIsNotReferral(f"user '{user.full_name}' is not '{referral.full_name}'`s sponsor")

    def get_referral(self, user_id: int, user: UserInterface):
        referral = self.repository.get_user_by_id(user_id)

        if not referral:
            raise UserDoesNotExist(f"no user with id '{user_id}'")

        referral.level = self.get_referral_level(referral, user)

        return ReferralSerializer(referral).data

    def set_referrals_count(self, referrals):
        for referral in referrals:
            referral.referrals = referral.first_level_referrals + sum(
                [self.repository.get_referrals_count(i, referral.id) for i in range(self.total_referal_level)]
            )

        return referrals

    def set_referral_level(self, referrals: list[ReferralInterface], level: int) -> list[ReferralInterface]:
        for referral in referrals:
            referral.level = level

        return referrals

    def get_referrals(self, user: UserInterface, level=None, sorted_by=None) -> list[UserInterface]:
        if level:
            level = self.validator.validate_referral_level(level)
        if sorted_by:
            sorted_by = self.validator.validate_sorted_by(sorted_by)

        if not level:
            referrals = []
            for i in range(self.total_referal_level):
                referrals.extend(self.set_referral_level(self.repository.get_referrals_by_level(user, i + 1), i + 1))

        else:
            referrals = self.repository.get_referrals_by_level(user, level)
            self.set_referral_level(referrals, level)

        referrals = self.set_referrals_count(referrals)

        if sorted_by:
            try:
                referrals = sort_list_by_attr(referrals, sorted_by)
            except ValueError:
                raise InvalidSortedByField(f"User has no field '{sorted_by}'")

        return referrals


def get_referral_service() -> ReferralService:
    return ReferralService(get_user_validator(), get_user_repository())
