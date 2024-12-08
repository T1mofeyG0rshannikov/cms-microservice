from application.texts.errors import UserErrors
from domain.referrals.referral import UserInterface
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist, UserNotAdmin
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository


class GetAdminUser:
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, username: str, password: str) -> UserInterface:
        user1 = self.repository.get_user_by_email(username)
        user2 = self.repository.get_user_by_phone(username)

        if not user1 and not user2:
            raise UserDoesNotExist(UserErrors.incorrect_login)

        user = user1 if user1 else user2

        if not user.check_password(password):
            raise IncorrectPassword(UserErrors.incorrect_password)

        if not user.is_superuser:
            raise UserNotAdmin(UserErrors.insufficient_permissions)

        return user


def get_get_admin_user_interactor(repository: UserRepositoryInterface = get_user_repository()) -> GetAdminUser:
    return GetAdminUser(repository)
