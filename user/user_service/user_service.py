from domens.domain_service.domain_service import get_domain_service
from domens.domain_service.domain_service_interface import DomainServiceInterface
from user.models.user import User
from user.user_repository.repository import get_user_repository
from user.user_repository.repository_interface import UserRepositoryInterface
from user.user_service.user_service_interface import UserServiceInterface


class UserService(UserServiceInterface):
    def __init__(self, domain_service: DomainServiceInterface, repository: UserRepositoryInterface):
        self.domain_service = domain_service
        self.repository = repository

    def get_user_from_site(self, site, domain) -> User | None:
        if domain == self.domain_service.get_domain_model():
            return self.repository.get_supersponsor()

        if site:
            return site.user

        return None


def get_user_service() -> UserService:
    return UserService(get_domain_service(), get_user_repository())
