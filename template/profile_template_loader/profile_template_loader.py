from domens.domain_service.domain_service import DomainService
from template.profile_template_loader.profile_template_loader_interface import (
    ProfileTemplateLoaderInterface,
)
from template.template_loader.base_template_loader import BaseTemplateLoader
from template.template_loader.tempate_context_processor.template_context_processor import (
    TemplateContextProcessor,
    get_template_context_processor,
)


class ProfileTemplateLoader(BaseTemplateLoader, ProfileTemplateLoaderInterface):
    app_name = "account"

    def __init__(self, context_processor: TemplateContextProcessor):
        self.context_processor = context_processor

    def load_template(self, template_name: str, request=None, context=None) -> str | None:
        return super().load_template(self.app_name, template_name, request, context)

    def get_title(self, page_title):
        return f"{page_title} | {DomainService.get_site_name()}"

    def load_profile_template(self, request):
        context = self.context_processor.get_profile_template_context(request)

        return {
            "content": self.load_template(template_name="profile-content", request=request, context=context),
            "title": self.get_title("Обзор"),
        }

    def load_refs_template(self, request):
        context = self.context_processor.get_refs_template_context(request)

        return {
            "content": self.load_template(template_name="refs-content", request=request, context=context),
            "title": self.get_title("Мои рефералы"),
        }

    def load_site_template(self, request):
        context = self.context_processor.get_site_template_context(request)

        return {
            "content": self.load_template(template_name="site-content", request=request, context=context),
            "title": self.get_title("Мой сайт"),
        }

    def load_manuals_template(self, request):
        context = self.context_processor.get_manuals_template_context(request)

        return {
            "content": self.load_template(template_name="manuals-content", request=request, context=context),
            "title": self.get_title("Руководства"),
        }


def get_profile_template_loader() -> ProfileTemplateLoader:
    return ProfileTemplateLoader(get_template_context_processor())
