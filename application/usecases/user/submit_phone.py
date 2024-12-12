from application.texts.errors import UserErrorsMessages
from domain.email.repository import SystemRepositoryInterface
from domain.user.exceptions import InvalidConfirmPhoneCode
from domain.user.repository import UserRepositoryInterface


class ConfirmUserPhone:
    def __init__(self, system_repository: SystemRepositoryInterface, user_repository: UserRepositoryInterface) -> None:
        self.system_repository = system_repository
        self.user_repository = user_repository

    def __call__(self, user_id: int, code: str) -> None:
        valid_code = self.system_repository.get_user_confirm_phone_code(user_id=user_id)

        if valid_code == code:
            self.user_repository.confirm_phone(user_id)
            self.system_repository.delete_user_confirm_phone_code(user_id)

        else:
            raise InvalidConfirmPhoneCode(UserErrorsMessages.wrong_code)


def get_confirm_phone_interactor(
    system_repository: SystemRepositoryInterface, user_repository: UserRepositoryInterface
) -> ConfirmUserPhone:
    return ConfirmUserPhone(system_repository=system_repository, user_repository=user_repository)
