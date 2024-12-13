from dataclasses import dataclass

from application.texts.errors import UserErrorsMessages
from domain.domains.domain import DomainInterface
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.user.exceptions import (
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.repository import UserRepositoryInterface
from domain.user.sites.site import SiteInterface
from domain.user.sites.site_repository import SiteRepositoryInterface
from domain.user.user import UserInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.site_repository import get_site_repository
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.url_parser.base_url_parser import UrlParserInterface
from infrastructure.url_parser.url_parser import get_url_parser


@dataclass
class TokenToSetPasswordResponse:
    token_to_set_password: str


class Register:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        site_repository: SiteRepositoryInterface,
        url_parser: UrlParserInterface,
        jwt_processor: JwtProcessorInterface,
    ) -> None:
        self.user_repository = user_repository
        self.domain_repository = domain_repository
        self.site_repository = site_repository
        self.url_parser = url_parser
        self.jwt_processor = jwt_processor

    def __call__(self, phone: str, email: str, host: str) -> TokenToSetPasswordResponse:
        user_with_phone = self.user_repository.get(phone=phone)
        user_with_email = self.user_repository.get(email=email)

        if user_with_email is not None and user_with_email.email_is_confirmed:
            raise UserWithEmailAlreadyExists(UserErrorsMessages.user_with_email_alredy_exists)

        elif user_with_phone is not None and user_with_phone.phone_is_confirmed:
            raise UserWithPhoneAlreadyExists(UserErrorsMessages.user_with_phone_alredy_exists)

        domain = self.get_domain_model_from_request(host)
        site = self.get_site_model(host)
        sponsor = self.get_user_from_site(site, domain)

        user = self.user_repository.create(
            phone=phone, email=email, register_on_site=site, register_on_domain=domain, sponsor=sponsor
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
        if not subdomain:
            return None

        return self.site_repository.get(subdomain=subdomain)

    def get_user_from_site(self, site: SiteInterface, domain: DomainInterface) -> UserInterface:
        if domain == self.domain_repository.get_domain(is_partners=False):
            return self.user_repository.get(supersponsor=True)

        if site:
            return site.user

        return None


def get_register_interactor(
    user_repository: UserRepositoryInterface = get_user_repository(),
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    site_repository: SiteRepositoryInterface = get_site_repository(),
    jwt_processor: JwtProcessorInterface = get_jwt_processor(),
    url_parser: UrlParserInterface = get_url_parser(),
) -> Register:
    return Register(user_repository, domain_repository, site_repository, url_parser, jwt_processor)
