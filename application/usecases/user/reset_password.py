from application.texts.errors import Errors
from domain.referrals.referral import UserInterface
from domain.user.exceptions import InvalidJwtToken
from domain.user.repository import UserRepositoryInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository


class ValidResetPasswordToken:
    def __init__(self, jwt_processor: JwtProcessorInterface, repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.repository = repository

    def __call__(self, token: str) -> UserInterface:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(Errors.wrong_reset_password_link)

        user = self.repository.get_user_by_id(payload["id"])
        if user is None:
            raise InvalidJwtToken(Errors.wrong_reset_password_link)

        return user


class ResetPassword:
    def __init__(self, jwt_processor: JwtProcessorInterface, repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.repository = repository

    def __call__(self, token: str, new_password: str) -> tuple[UserInterface, dict]:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(Errors.expired_set_password_token)

        user = self.repository.set_password(payload["id"], new_password)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        return user, access_token


def get_reset_password_interactor(
    jwt_processor: JwtProcessorInterface = get_jwt_processor(),
    user_repository: UserRepositoryInterface = get_user_repository(),
) -> ResetPassword:
    return ResetPassword(jwt_processor, user_repository)


def get_valid_reset_pass_token_interactor(
    jwt_processor: JwtProcessorInterface = get_jwt_processor(),
    user_repository: UserRepositoryInterface = get_user_repository(),
) -> ValidResetPasswordToken:
    return ValidResetPasswordToken(jwt_processor, user_repository)
