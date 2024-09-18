from application.texts.errors import Errors
from domain.user.exceptions import InvalidJwtToken
from domain.user.interfaces import UserInterface
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from web.user.user_repository.repository_interface import UserRepositoryInterface


class ValidResetPasswordToken:
    def __init__(self, jwt_processor: JwtProcessorInterface, repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.repository = repository

    def __call__(self, token: str) -> UserInterface:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(Errors.wrong_reset_password_link.value)

        user = self.repository.get_user_by_id(payload["id"])
        if user is None:
            raise InvalidJwtToken(Errors.wrong_reset_password_link.value)

        return user


class ResetPassword:
    def __init__(self, jwt_processor: JwtProcessorInterface, repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.repository = repository

    def __call__(self, token: str, new_password: str):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(Errors.expired_set_password_token.value)

        user = self.repository.set_password(payload["id"], new_password)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        return user, access_token
