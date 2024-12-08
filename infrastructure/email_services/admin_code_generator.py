import random

from domain.email.repository import SystemRepositoryInterface
from infrastructure.persistence.repositories.system_repository import (
    get_system_repository,
)


class LoginCodeGenerator:
    def __init__(self, repository: SystemRepositoryInterface) -> None:
        self.repository = repository

    def generate_admin_login_code(self, email: str) -> int:
        code = random.randrange(100000, 1000000)
        return self.repository.update_or_create_admin_code(email=email, code=code)


def get_login_code_generator(repository: SystemRepositoryInterface = get_system_repository()) -> LoginCodeGenerator:
    return LoginCodeGenerator(repository)
