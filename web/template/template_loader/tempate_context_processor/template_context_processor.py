from django.http import HttpRequest

from application.services.domains.service import get_domain_service
from application.services.user.referrals_service import get_referral_service
from application.usecases.ideas.get_ideas import GetIdeas
from domain.domains.domain_service import DomainServiceInterface
from domain.products.repository import ProductRepositoryInterface
from domain.referrals.service import ReferralServiceInterface
from infrastructure.persistence.models.catalog.products import Product
from infrastructure.persistence.models.settings import (
    Domain,
    Messanger,
    SiteSettings,
    SocialNetwork,
    UserFont,
)
from infrastructure.persistence.models.user.product import UserProduct
from infrastructure.persistence.repositories.idea_repository import get_idea_repository
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from web.account.serializers import ReferralSerializer
from web.catalog.serializers import ProductSerializer, ProductsSerializer
from web.template.template_loader.tempate_context_processor.base_context_processor import (
    BaseContextProcessor,
)
from web.user.serializers import UserProductsSerializer

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(BaseContextProcessor, TemplateContextProcessorInterface):
    def __init__(
        self,
        referral_service: ReferralServiceInterface,
        domain_service: DomainServiceInterface,
        products_repository: ProductRepositoryInterface,
        get_ideas_interactor: GetIdeas,
    ):
        self.referral_service = referral_service
        self.products_repository = products_repository
        self.domain_service = domain_service
        self.get_ideas_interactor = get_ideas_interactor

    def get_change_user_form_context(self, request: HttpRequest):
        context = self.get_context(request)

        context["messangers"] = Messanger.objects.select_related("social_network").all()

        return context

    def get_change_site_form_context(self, request: HttpRequest):
        context = self.get_context(request)

        context["fonts"] = UserFont.objects.all()

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]
        context["domains"] = Domain.objects.values("domain", "id").filter(is_partners=True)

        return context

    def get_change_socials_form_context(self, request: HttpRequest):
        context = self.get_context(request)
        context["socials"] = SocialNetwork.objects.all()

        return context

    def get_referral_popup_context(self, request: HttpRequest):
        context = self.get_context(request)

        user_id = request.GET.get("user_id")

        context["user"] = ReferralSerializer(self.referral_service.get_referral(user_id, request.user)).data

        return context

    def get_choice_product_form(self, request: HttpRequest):
        context = self.get_context(request)
        organization = request.GET.get("organization")

        context["organizations"] = self.products_repository.get_enabled_organizations(request.user.id)

        self.products_repository.get_enabled_products_to_create(request.user.id, organization)

        context["products"] = ProductsSerializer(
            self.products_repository.get_enabled_products_to_create(request.user.id, organization), many=True
        ).data

        return context

    def get_create_user_product_form(self, request: HttpRequest):
        context = self.get_context(request)
        context["site_name"] = self.domain_service.get_site_name()

        product_id = request.GET.get("product")
        try:
            product = self.products_repository.get_product_by_id(product_id)
            context["product"] = ProductSerializer(product).data

            if UserProduct.objects.filter(user=request.user, product=product, deleted=False).exists():
                context["user_product"] = UserProductsSerializer(
                    UserProduct.objects.filter(user=request.user, product=product).first()
                ).data

        except Product.DoesNotExist:
            pass

        return context

    def get_product_description_popup(self, request: HttpRequest):
        product_id = request.GET.get("product")
        context = dict()
        context["product"] = (
            Product.objects.select_related("organization")
            .values("partner_description", "organization__partner_program")
            .get(id=product_id)
        )

        return context

    def get_delete_product_popup(self, request: HttpRequest):
        product_id = request.GET.get("product")
        context = dict()
        context["product"] = UserProduct.objects.values("id").get(id=product_id)

        return context

    def get_create_idea_form(self, request: HttpRequest):
        context = {}

        idea_id = request.GET.get("idea")

        context["idea"] = self.get_ideas_interactor.repository.get_idea(idea_id)
        return context


def get_template_context_processor(
    referral_service: ReferralServiceInterface = get_referral_service(),
    products_repository: ProductRepositoryInterface = get_product_repository(),
    domain_service: DomainServiceInterface = get_domain_service(),
    get_ideas_interactor: GetIdeas = GetIdeas(get_idea_repository()),
) -> TemplateContextProcessorInterface:
    return TemplateContextProcessor(
        referral_service=referral_service,
        products_repository=products_repository,
        domain_service=domain_service,
        get_ideas_interactor=get_ideas_interactor,
    )
