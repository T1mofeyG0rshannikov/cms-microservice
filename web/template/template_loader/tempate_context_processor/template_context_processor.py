from django.http import HttpRequest

from application.services.user.referrals_service import get_referral_service
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from domain.referrals.service import ReferralServiceInterface
from domain.user.idea_repository import IdeaRepositoryInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.idea_repository import get_idea_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.settings_repository import (
    get_settings_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.serializers import ReferralSerializer
from web.catalog.serializers import ProductSerializer, ProductsSerializer
from web.user.serializers import UserProductsSerializer

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(TemplateContextProcessorInterface):
    def __init__(
        self,
        domain_repository: DomainRepositoryInterface,
        products_repository: ProductRepositoryInterface,
        user_products_repository: UserProductRepositoryInterface,
    ) -> None:
        self.domain_repository = domain_repository
        self.products_repository = products_repository
        self.user_products_repository = user_products_repository

    def get_change_user_form_context(
        self, request: HttpRequest, settings_repository: SettingsRepositoryInterface = get_settings_repository()
    ):
        return {"user": request.user, "messangers": settings_repository.get_messangers()}

    def get_change_site_form_context(
        self, request: RequestInterface, settings_repository: SettingsRepositoryInterface = get_settings_repository()
    ):
        return {
            "site": request.user.site,
            "fonts": settings_repository.get_user_fonts(),
            "default_user_size": settings_repository.get_settings().default_users_font_size,
            "domains": settings_repository.get_partner_domains(),
        }

    def get_change_socials_form_context(
        self, request: RequestInterface, settings_repository: SettingsRepositoryInterface = get_settings_repository()
    ):
        return {"site": request.user.site, "socials": settings_repository.get_social_networks()}

    def get_referral_popup_context(
        self, request: HttpRequest, referral_service: ReferralServiceInterface = get_referral_service()
    ):
        user_id = request.GET.get("user_id")

        return {"user": ReferralSerializer(referral_service.get_referral(user_id, request.user)).data}

    def get_choice_product_form(self, request: HttpRequest):
        organization = request.GET.get("organization")

        return {
            "organizations": self.products_repository.get_enabled_organizations(request.user.id),
            "products": ProductsSerializer(
                self.products_repository.get_enabled_products_to_create(request.user.id, organization), many=True
            ).data,
        }

    def get_create_user_product_form(self, request: HttpRequest):
        context = {}
        context["user"] = request.user
        context["site_name"] = self.domain_repository.get_site_name()

        product_id = request.GET.get("product")

        product = self.products_repository.get(id=product_id)
        if product is None:
            return context

        context["product"] = ProductSerializer(product).data

        if self.user_products_repository.exists(product_id=product_id, user_id=request.user.id):
            context["user_product"] = UserProductsSerializer(
                self.user_products_repository.get(product_id=product_id, user_id=request.user.id)
            ).data

        return context

    def get_product_description_popup(self, request: HttpRequest):
        product_id = request.GET.get("product")
        return {"product": self.products_repository.get_product_for_popup(product_id)}

    def get_create_idea_form(
        self, request: HttpRequest, idea_repository: IdeaRepositoryInterface = get_idea_repository()
    ):
        idea_id = request.GET.get("idea")

        return {"idea": idea_repository.get(idea_id)}


def get_context_processor(
    products_repository: ProductRepositoryInterface = get_product_repository(),
    user_products_repository: UserProductRepositoryInterface = get_user_product_repository(),
    domain_repositroy: DomainRepositoryInterface = get_domain_repository(),
) -> TemplateContextProcessorInterface:
    return TemplateContextProcessor(
        products_repository=products_repository,
        domain_repository=domain_repositroy,
        user_products_repository=user_products_repository,
    )
