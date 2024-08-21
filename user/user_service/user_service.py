from domens.domain_service.domain_service import get_domain_service
from domens.domain_service.domain_service_interface import DomainServiceInterface
from user.models.user import User
from user.user_service.user_service_interface import UserServiceInterface


class UserService(UserServiceInterface):
    def __init__(self, domain_service: DomainServiceInterface):
        self.domain_service = domain_service

    def get_user_from_site(self, site, domain) -> User:
        if domain == self.domain_service.get_domain_model():
            return User.objects.filter(supersponsor=True).first()

        return site.user


def get_user_service() -> UserService:
    return UserService(get_domain_service())
