from application.texts.errors import ErrorsMessages
from domain.referrals.referral import UserInterface
from domain.user.exceptions import InvalidJwtToken
from domain.user.repository import UserRepositoryInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository


class ValidResetPasswordToken:
    def __init__(self, jwt_processor: JwtProcessorInterface, user_repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.user_repository = user_repository

    def __call__(self, token: str) -> UserInterface:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(ErrorsMessages.wrong_reset_password_link)

        user = self.user_repository.get(id=payload["id"])
        if user is None:
            raise InvalidJwtToken(ErrorsMessages.wrong_reset_password_link)

        return user


class ResetPassword:
    def __init__(self, jwt_processor: JwtProcessorInterface, user_repository: UserRepositoryInterface) -> None:
        self.jwt_processor = jwt_processor
        self.user_repository = user_repository

    def __call__(self, token: str, new_password: str) -> tuple[UserInterface, dict]:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            raise InvalidJwtToken(ErrorsMessages.expired_set_password_token)

        user = self.user_repository.set_password(payload["id"], new_password)

        access_token = self.jwt_processor.create_token(data={"sub": user.username, "id": user.id})

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
