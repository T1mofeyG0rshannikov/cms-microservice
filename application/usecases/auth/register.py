from typing import Any

from domain.domains.domain import DomainInterface, SiteInterface
from domain.domains.repository import DomainRepositoryInterface
from domain.user.exceptions import (
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from domain.user.user import UserInterface


class Register:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        url_parser,
        jwt_processor,
    ) -> None:
        self.user_repository = user_repository
        self.domain_repository = domain_repository
        self.url_parser = url_parser
        self.jwt_processor = jwt_processor

    def get_domain_model_from_request(self, host):
        domain = self.url_parser.get_domain_from_host(host)
        return self.domain_repository.get_domain(domain)

    def get_site_model(self, host):
        subdomain = self.url_parser.get_subdomain_from_host(host)
        print(subdomain, self.domain_repository.get_site(subdomain))
        return self.domain_repository.get_site(subdomain)

    def get_user_from_site(self, site: SiteInterface, domain: DomainInterface) -> UserInterface:
        if domain == self.domain_repository.get_domain_model():
            return self.user_repository.get_supersponsor()

        if site:
            return site.user

        return None

    def __call__(self, fields: dict[str, Any], host: str):
        phone = fields.get("phone")
        email = fields.get("email")

        user_with_phone = self.user_repository.get_user_by_phone(phone)
        user_with_email = self.user_repository.get_user_by_email(email)

        if user_with_email is not None and user_with_email.email_is_confirmed:
            raise UserWithEmailAlreadyExists()

        elif user_with_phone is not None and user_with_phone.phone_is_confirmed:
            raise UserWithPhoneAlreadyExists()

        domain = self.get_domain_model_from_request(host)
        site = self.get_site_model(host)
        sponsor = self.get_user_from_site(site, domain)

        user = self.user_repository.create_user(
            **fields, register_on_site=site, register_on_domain=domain, sponsor=sponsor
        )

        if user:
            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return token_to_set_password

        return None
