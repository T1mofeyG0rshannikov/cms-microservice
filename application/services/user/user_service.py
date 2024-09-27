from application.texts.errors import UserErrors
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist
from domain.user.repository import UserRepositoryInterface
from domain.user.service import UserServiceInterface
from domain.user.user import UserInterface


class UserService(UserServiceInterface):
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository

    def get_user(self, login: str, password: str) -> UserInterface:
        user1 = self.repository.get_user_by_email(login)
        user2 = self.repository.get_user_by_phone(login)

        if not user1 and not user2:
            raise UserDoesNotExist(UserErrors.incorrect_login.value)

        if user1:
            user = user1
        if user2:
            user = user2

        if not user.check_password(password):
            raise IncorrectPassword("Неверный пароль")

        return user
