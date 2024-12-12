from application.texts.errors import UserErrorsMessages
from domain.user.exceptions import UserDoesNotExist
from domain.user.repository import UserRepositoryInterface
from domain.user.user import UserInterface
from domain.user.validator import UserValidatorInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.user.validator import get_user_validator


class Login:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        validator: UserValidatorInterface,
        jwt_processor: JwtProcessorInterface,
    ) -> None:
        self.user_repository = user_repository
        self.validator = validator
        self.jwt_processor = jwt_processor

    def __call__(self, phone_or_email: str, password: str) -> tuple[dict, UserInterface]:
        if self.validator.is_valid_phone(phone_or_email):
            user = self.user_repository.get(phone=phone_or_email)
            if user is None:
                raise UserDoesNotExist(UserErrorsMessages.user_by_phone_not_found)

        elif self.validator.is_valid_email(phone_or_email):
            user = self.user_repository.get(email=phone_or_email)
            if user is None:
                raise UserDoesNotExist(UserErrorsMessages.user_by_email_not_found)

        else:
            raise UserDoesNotExist(UserErrorsMessages.incorrect_login)

        if not self.user_repository.verify_password(user.id, password):
            raise UserDoesNotExist(UserErrorsMessages.incorrect_password)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        return access_token, user


def get_login_interactor(
    user_repository: UserRepositoryInterface = get_user_repository(),
    user_validator: UserValidatorInterface = get_user_validator(),
    jwt_processor: JwtProcessorInterface = get_jwt_processor(),
) -> Login:
    return Login(user_repository, user_validator, jwt_processor)
