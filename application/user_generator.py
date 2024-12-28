import random

import unidecode
from russian_names import RussianNames

from domain.domains.domain import DomainInterface
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.tests.test_user_set import TestUserSetInterface
from domain.user.entities import SiteInterface, UserInterface
from domain.user.repository import UserRepositoryInterface
from domain.user.sites.site_repository import SiteRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.site_repository import get_site_repository
from infrastructure.persistence.repositories.user_repository import get_user_repository


class UserGeneratorInterface:
    pass


class UserGenerator(UserGeneratorInterface):
    def __init__(
        self,
        site_repository: SiteRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        test_user_set: TestUserSetInterface,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self.site_repository = site_repository
        self.domain_repository = domain_repository
        self.test_user_set = test_user_set
        self.user_repository = user_repository

    @staticmethod
    def generate_email(user_slug: str) -> str:
        return f"{user_slug}@mail.ru"

    @staticmethod
    def generate_phone() -> str:
        s = str(random.randint(0, 1_000_000_000))
        s = "0" * (9 - len(s)) + s

        return f"+79{s}"

    @staticmethod
    def ger_user_english_slug(name: str, second_name: str) -> str:
        return unidecode.unidecode(name) + unidecode.unidecode(second_name)

    def create_test_users(self, count: int) -> None:
        rn = RussianNames(count=count, patronymic=False, transliterate=False)

        partner_domain = self.domain_repository.get_domain(is_partners=True)
        sites = list(self.site_repository.all())

        for user in rn:
            name, second_name = user.split(" ")
            user = self.create_test_user(
                name=name, second_name=second_name, partner_domain=partner_domain, site=random.choice(sites)
            )

            if user:
                sites.append(self.create_test_site(user, partner_domain))

    def create_test_site(self, user: UserInterface, partner_domain: DomainInterface) -> SiteInterface:
        subdomain = self.ger_user_english_slug(user.username, user.second_name)

        site, _ = self.site_repository.update_or_create(
            domain=partner_domain,
            subdomain=subdomain,
            is_active=True,
            use_default_settings=True,
            advertising_channel=subdomain,
            user_id=user.id,
            name=subdomain,
        )

        return site

    def create_test_user(
        self, name: str, second_name: str, partner_domain: DomainInterface, site: SiteInterface
    ) -> UserInterface | None:
        user_slug = self.ger_user_english_slug(name, second_name)
        email = self.generate_email(user_slug)
        phone = self.generate_phone()

        try:
            user = self.user_repository.create(
                username=name,
                second_name=second_name,
                email=email,
                email_is_confirmed=True,
                phone=phone,
                phone_is_confirmed=True,
                register_on_domain=partner_domain,
                register_on_site=site,
                sponsor=site.user,
                test=True,
                test_set=self.test_user_set,
            )

            return user
        except:
            return None


def get_user_generator(
    test_user_set,
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
    site_repository: SiteRepositoryInterface = get_site_repository(),
    repository: UserRepositoryInterface = get_user_repository(),
) -> UserGeneratorInterface:
    return UserGenerator(
        test_user_set=test_user_set,
        domain_repository=domain_repository,
        user_repository=repository,
        site_repository=site_repository,
    )
