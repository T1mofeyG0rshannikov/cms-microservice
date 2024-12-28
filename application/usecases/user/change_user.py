from dataclasses import dataclass

from application.texts.errors import UserErrorsMessages
from domain.common.screen import FileInterface
from domain.referrals.referral import UserInterface
from domain.user.exceptions import (
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository


@dataclass
class ChangeUserDTO:
    changed_email: bool


class ChangeUser:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    def __call__(
        self,
        user: UserInterface,
        phone: str,
        email: str,
        username: str,
        second_name: str,
        profile_picture: FileInterface | None = None,
        social_network: int | None = None,
        adress: str | None = None,
    ) -> ChangeUserDTO:
        user_with_phone = self.user_repository.get(phone=phone)
        user_with_email = self.user_repository.get(email=email)

        if user_with_email != user and user_with_email and user_with_email.email_is_confirmed:
            raise UserWithEmailAlreadyExists(UserErrorsMessages.user_with_email_alredy_exists)

        elif user_with_phone != user and user_with_phone and user_with_phone.phone_is_confirmed:
            raise UserWithPhoneAlreadyExists(UserErrorsMessages.user_with_phone_alredy_exists)

        phone_is_confirmed = False if phone != user.phone else user.phone_is_confirmed

        self.user_repository.update(
            id=user.id,
            username=username,
            second_name=second_name,
            phone=phone,
            phone_is_confirmed=phone_is_confirmed,
            profile_picture=profile_picture,
        )

        if social_network and adress:
            self.user_repository.update_or_create_messanger(user_id=user.id, messanger_id=social_network, adress=adress)

        if user.email_is_confirmed and email != user.email:
            self.user_repository.change_email(user.id, email)

            return ChangeUserDTO(changed_email=True)

        self.user_repository.change_email(user.id, email)

        return ChangeUserDTO(changed_email=False)


def get_change_user_interactor(repository: UserRepositoryInterface = get_user_repository()) -> ChangeUser:
    return ChangeUser(repository)
