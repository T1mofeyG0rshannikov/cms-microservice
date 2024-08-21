from typing import Protocol

from domens.domain_service.domain_service_interface import DomainServiceInterface
from user.models.user import User


class UserServiceInterface(Protocol):
    domain_service: DomainServiceInterface

    def get_user_from_site(self, site, domain) -> User:
        raise NotImplementedError()
