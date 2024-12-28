from application.dto.change_password import ChangePasswordResponse
from application.texts.errors import UserErrorsMessages
from domain.user.entities import UserInterface
from domain.user.exceptions import IncorrectPassword, InvalidPassword
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface


class ChangePassword:
    def __init__(self, jwt_processor: JwtProcessorInterface) -> None:
        self.jwt_processor = jwt_processor

    def __call__(
        self, password: str, repeat_password: str, current_password: str, user: UserInterface
    ) -> ChangePasswordResponse:
        if len(password) < 6:
            raise InvalidPassword(UserErrorsMessages.to_short_password)

        if not user.check_password(current_password):
            raise IncorrectPassword(UserErrorsMessages.incorrect_password)

        if password != repeat_password:
            raise IncorrectPassword(UserErrorsMessages.passwords_dont_match)

        user.set_password(password)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        return ChangePasswordResponse(user=user, access_token=access_token)


def get_change_password_interactor(jwt_processor: JwtProcessorInterface = get_jwt_processor()) -> ChangePassword:
    return ChangePassword(jwt_processor)
