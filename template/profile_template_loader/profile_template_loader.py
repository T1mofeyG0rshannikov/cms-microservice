from template.profile_template_loader.context_processor.context_processor import (
    ProfileTemplateContextProcessor,
    get_profile_template_context_processor,
)
from template.profile_template_loader.profile_template_loader_interface import (
    ProfileTemplateLoaderInterface,
)
from template.template_loader.base_template_loader import BaseTemplateLoader


class ProfileTemplateLoader(BaseTemplateLoader, ProfileTemplateLoaderInterface):
    app_name = "account"
    template_folder = "contents"

    def __init__(self, context_processor: ProfileTemplateContextProcessor):
        self.context_processor = context_processor

    def load_template(self, template_name: str, request=None, context=None) -> str | None:
        return super().load_template(self.app_name, self.template_folder + "/" + template_name, request, context)

    def get_title(self, page_title):
        return f"{page_title} | {self.context_processor.domain_service.get_site_name()}"

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

    def load_products_template(self, request):
        context = self.context_processor.get_products_template_context(request)

        return {
            "content": self.load_template(template_name="products-content", request=request, context=context),
            "title": self.get_title("Продукты"),
        }


def get_profile_template_loader() -> ProfileTemplateLoader:
    return ProfileTemplateLoader(get_profile_template_context_processor())
