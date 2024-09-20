from application.texts.errors import UserErrors
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist, UserNotAdmin
from domain.user.referral import UserInterface
from domain.user.repository import UserRepositoryInterface


class GetAdminUser:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def __call__(self, username: str, password: str) -> UserInterface:
        user1 = self.repository.get_user_by_email(username)
        user2 = self.repository.get_user_by_phone(username)

        print(user1)
        print(user2)
        if not user1 and not user2:
            raise UserDoesNotExist(UserErrors.incorrect_login.value)

        if user1:
            user = user1
        if user2:
            user = user2

        if not user.check_password(password):
            raise IncorrectPassword("Неверный пароль")

        print(user)
        if not user.is_superuser:
            raise UserNotAdmin("Недостаточно прав")

        return user
