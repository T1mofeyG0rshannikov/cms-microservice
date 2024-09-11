from typing import Any

from user.exceptions import UserWithEmailAlreadyExists, UserWithPhoneAlreadyExists
from user.interfaces import UserInterface
from user.user_repository.repository_interface import UserRepositoryInterface
from utils.errors import UserErrors


class ChangeUser:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def __call__(self, user: UserInterface, fields: dict[str, Any]) -> bool:
        phone = fields.get("phone")
        email = fields.get("email")

        user_with_phone = self.repository.get_user_by_phone(phone)
        user_with_email = self.repository.get_user_by_email(email)

        if user_with_email != user and user_with_email and user_with_email.email_is_confirmed:
            raise UserWithEmailAlreadyExists(UserErrors.username_with_email_alredy_exists.value)

        elif user_with_phone != user and user_with_phone and user_with_phone.phone_is_confirmed:
            raise UserWithPhoneAlreadyExists(UserErrors.username_with_phone_alredy_exists.value)

        self.repository.update_user(
            id=user.id,
            username=fields.get("username"),
            second_name=fields.get("second_name"),
            phone=phone,
            profile_picture=fields.get("profile_picture"),
        )

        if fields.get("social_network"):
            social_network = fields.get("social_network")
            adress = fields.get("adress")

            self.repository.update_or_create_user_messanger(user_id=user.id, messanger_id=social_network, adress=adress)

        if user.email_is_confirmed and email != user.email:
            self.repository.change_user_email(user.id, email)

            return True

        self.repository.change_user_email(user.id, email)

        return False
