from collections.abc import Iterable

from domain.referrals.referral import ReferralInterface, UserInterface
from domain.referrals.repository import ReferralRepositoryInterface
from domain.referrals.service import ReferralServiceInterface
from domain.user.exceptions import UserDoesNotExist, UserIsNotReferral
from domain.user.validator import UserValidatorInterface
from infrastructure.persistence.repositories.referral_repository import (
    get_referral_repository,
)
from infrastructure.user.validator import get_user_validator


class ReferralService(ReferralServiceInterface):
    total_referal_level: int = 3

    def __init__(self, validator: UserValidatorInterface, repository: ReferralRepositoryInterface) -> None:
        self.validator = validator
        self.repository = repository

    def get_referral_level(self, referral: ReferralInterface, user: UserInterface) -> int:
        sponsor = referral.sponsor
        for i in range(self.total_referal_level):
            if sponsor.id == user.id:
                return i + 1

            sponsor = sponsor.sponsor

        raise UserIsNotReferral(f"user '{user.full_name}' is not '{referral.full_name}'`s sponsor")

    def get_referral(self, user_id: int, user: UserInterface) -> ReferralInterface:
        referral = self.repository.get_referral_by_id(user_id)

        if not referral:
            raise UserDoesNotExist(f"no user with id '{user_id}'")

        referral.level = self.get_referral_level(referral, user)

        return referral

    def get_referrals(self, user_id: int, level: int = None, sorted_by="created_at") -> Iterable[ReferralInterface]:
        if sorted_by:
            sorted_by = self.validator.validate_sorted_by(sorted_by)

        if level:
            level = self.validator.validate_referral_level(level)

        return self.repository.get_referrals(user_id, self.total_referal_level, level, sorted_by)


def get_referral_service(
    validator: UserValidatorInterface = get_user_validator(),
    repository: ReferralRepositoryInterface = get_referral_repository(),
) -> ReferralServiceInterface:
    return ReferralService(validator=validator, repository=repository)
