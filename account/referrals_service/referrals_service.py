from user.exceptions import UserIsNotReferral


class ReferralService:
    total_referal_level: int = 3

    def get_referral_level(self, referral, user):
        sponsor = referral.sponsor
        for i in range(self.total_referal_level):
            if sponsor.id == user.id:
                return i + 1

            sponsor = sponsor.sponsor

        raise UserIsNotReferral(f"user '{user.full_name}' is not '{referral.full_name}'`s sponsor")


def get_referral_service() -> ReferralService:
    return ReferralService()
