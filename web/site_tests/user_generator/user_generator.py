import random

import unidecode
from russian_names import RussianNames
from user.models.site import Site
from user.models.user import User

from application.services.domains.service import get_domain_service
from domain.domains.interfaces.domain_service_interface import DomainServiceInterface


class UserGenerator:
    def __init__(self, domain_service: DomainServiceInterface, test_user_set):
        self.domain_service = domain_service
        self.test_user_set = test_user_set
        self.partner_domain = self.domain_service.get_partner_domain_model()

    def ger_user_english_slug(self, name, second_name):
        return unidecode.unidecode(name) + unidecode.unidecode(second_name)

    def create_test_users(self, count):
        rn = RussianNames(count=count, patronymic=False, transliterate=False)
        for user in rn:
            name, second_name = user.split(" ")
            user = self.create_test_user(name=name, second_name=second_name)

            if user:
                self.create_test_site(user)

    @staticmethod
    def generate_email(user_slug):
        return f"{user_slug}@mail.ru"

    @staticmethod
    def generate_phone():
        return f"+79{''.join(random.choices('0123456789', k=9))}"

    def create_test_site(self, user):
        subdomain = self.ger_user_english_slug(user.username, user.second_name)

        Site.objects.create(
            domain=self.partner_domain,
            subdomain=subdomain,
            is_active=True,
            use_default_settings=True,
            advertising_channel=subdomain,
            user=user,
            name=subdomain,
        )

    def create_test_user(self, name, second_name):
        user_slug = self.ger_user_english_slug(name, second_name)
        email = self.generate_email(user_slug)
        phone = self.generate_phone()

        partner_domain = self.domain_service.get_partner_domain_model()
        site = self.domain_service.get_random_site()

        try:
            user = User.objects.create(
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


def get_user_generator(test_user_set) -> UserGenerator:
    return UserGenerator(get_domain_service(), test_user_set)
