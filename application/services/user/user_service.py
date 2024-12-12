from application.texts.errors import UserErrorsMessages
from domain.user.exceptions import IncorrectPassword, UserDoesNotExist
from domain.user.repository import UserRepositoryInterface
from domain.user.service import UserServiceInterface
from domain.user.user import UserInterface


class UserService(UserServiceInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    def get_user(self, login: str, password: str) -> UserInterface:
        user1 = self.user_repository.get(email=login)
        user2 = self.user_repository.get(phone=login)

        if not user1 and not user2:
            raise UserDoesNotExist(UserErrorsMessages.incorrect_login)

        user = user1 if user1 else user2

        if not user.check_password(password):
            raise IncorrectPassword(UserErrorsMessages.incorrect_password)

        return user
