from typing import Any

from django.http import HttpRequest

from domain.domains.domain_repository import DomainRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from web.template.profile_template_loader.context_processor.context_processor import (
    get_profile_context_processor,
)
from web.template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from web.template.profile_template_loader.profile_template_loader_interface import (
    ProfileTemplateLoaderInterface,
)
from web.template.template_loader.base_template_loader import BaseTemplateLoader


class ProfileTemplateLoader(BaseTemplateLoader, ProfileTemplateLoaderInterface):
    app_name = "account"
    template_folder = "contents"

    def __init__(
        self, context_processor: ProfileTemplateContextProcessorInterface, domain_repositrory: DomainRepositoryInterface
    ) -> None:
        self.context_processor = context_processor
        self.domain_repository = domain_repositrory

    def load_template(self, app_name: str, template_name: str, context: dict[str, Any] | None = None) -> str | None:
        return super().load_template(app_name, self.template_folder + "/" + template_name, context)

    def get_title(self, page_title: str) -> str:
        return f"{page_title} | {self.domain_repository.get_site_name()}"

    def load_profile_template(self, request: HttpRequest):
        context = self.context_processor.get_profile_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="profile-content", context=context),
            "title": self.get_title("Обзор"),
        }

    def load_refs_template(self, request: HttpRequest):
        context = self.context_processor.get_refs_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="refs-content", context=context),
            "title": self.get_title("Мои рефералы"),
        }

    def load_site_template(self, request: HttpRequest):
        context = self.context_processor.get_site_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="site-content", context=context),
            "title": self.get_title("Мой сайт"),
        }

    def load_manuals_template(self, request: HttpRequest):
        context = self.context_processor.get_manuals_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="manuals-content", context=context),
            "title": self.get_title("Руководства"),
        }

    def load_products_template(self, request: HttpRequest):
        context = self.context_processor.get_products_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="products-content", context=context),
            "title": self.get_title("Продукты"),
        }

    def load_ideas_template(self, request: HttpRequest):
        context = self.context_processor.get_ideas_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="ideas", context=context),
            "title": self.get_title("Обратная связь"),
        }

    def load_messanger_template(self, request: HttpRequest):
        context = self.context_processor.get_messanger_context(request)

        return {
            "content": self.load_template(app_name=self.app_name, template_name="messanger", context=context),
            "title": self.get_title("Мессенджер"),
        }


def get_profile_template_loader(
    context_processor: ProfileTemplateContextProcessorInterface = get_profile_context_processor(),
    domain_repository: DomainRepositoryInterface = get_domain_repository(),
) -> ProfileTemplateLoaderInterface:
    return ProfileTemplateLoader(context_processor=context_processor, domain_repositrory=domain_repository)
