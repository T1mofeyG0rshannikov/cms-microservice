from dataclasses import dataclass
from typing import Any

from application.common.base_url_parser import UrlParserInterface
from domain.domains.repository import DomainRepositoryInterface
from domain.domains.site import DomainInterface, SiteInterface
from domain.user.exceptions import (
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from domain.user.user import UserInterface
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface


@dataclass
class TokenToSetPasswordResponse:
    token_to_set_password: str


class Register:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        url_parser: UrlParserInterface,
        jwt_processor: JwtProcessorInterface,
    ) -> None:
        self.user_repository = user_repository
        self.domain_repository = domain_repository
        self.url_parser = url_parser
        self.jwt_processor = jwt_processor


    def __call__(self, fields: dict[str, Any], host: str) -> TokenToSetPasswordResponse:
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

            return TokenToSetPasswordResponse(token_to_set_password=token_to_set_password)

        return None
    
    def get_domain_model_from_request(self, host: str) -> DomainInterface:
        domain = self.url_parser.get_domain_from_host(host)
        return self.domain_repository.get_domain(domain)

    def get_site_model(self, host: str) -> SiteInterface:
        subdomain = self.url_parser.get_subdomain_from_host(host)
        return self.domain_repository.get_site(subdomain)

    def get_user_from_site(self, site: SiteInterface, domain: DomainInterface) -> UserInterface:
        if domain == self.domain_repository.get_domain_model():
            return self.user_repository.get_supersponsor()

        if site:
            return site.user

        return None

