from account.models import Messanger
from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from catalog.models.products import Product
from catalog.products_service.products_service import get_products_service
from catalog.products_service.products_service_interface import ProductsServiceInterface
from catalog.serializers import ProductSerializer
from domens.domain_service.domain_service import get_domain_service
from domens.domain_service.domain_service_interface import DomainServiceInterface
from materials.models import Document
from settings.models import Domain, SiteSettings, SocialNetwork, UserFont
from template.template_loader.tempate_context_processor.base_context_processor import (
    BaseContextProcessor,
)
from user.models.product import UserProduct

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(BaseContextProcessor, TemplateContextProcessorInterface):
    def __init__(
        self,
        referral_service: ReferralServiceInterface,
        products_service: ProductsServiceInterface,
        domain_service: DomainServiceInterface,
    ):
        self.referral_service = referral_service
        self.products_service = products_service
        self.domain_service = domain_service

    def get_change_user_form_context(self, request):
        context = self.get_context(request)

        context["messangers"] = Messanger.objects.select_related("social_network").all()

        return context

    def get_change_site_form_context(self, request):
        context = self.get_context(request)

        context["fonts"] = UserFont.objects.all()

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]
        context["domains"] = Domain.objects.values("domain", "id").filter(is_partners=True)

        return context

    def get_change_socials_form_context(self, request):
        context = self.get_context(request)
        context["socials"] = SocialNetwork.objects.all()

        return context

    def get_referral_popup_context(self, request):
        context = self.get_context(request)

        user_id = request.GET.get("user_id")

        context["user"] = self.referral_service.get_referral(user_id, request.user)

        return context

    def get_choice_product_form(self, request):
        context = self.get_context(request)
        context["organizations"] = self.products_service.get_enabled_organizations(request.user.id)
        context["products"] = self.products_service.get_enabled_products_to_create(request.user.id)

        return context

    def get_create_user_product_form(self, request):
        context = self.get_context(request)
        context["site_name"] = self.domain_service.get_site_name()

        product_id = request.GET.get("product")
        try:
            product = Product.objects.get(id=product_id)
            context["product"] = ProductSerializer(product).data

            if UserProduct.objects.filter(user=request.user, product=product, deleted=False).exists():
                context["user_product"] = UserProduct.objects.filter(user=request.user, product=product).first()

        except Product.DoesNotExist:
            pass

        return context

    def get_product_description_popup(self, request):
        product_id = request.GET.get("product")
        context = dict()
        context["product"] = (
            Product.objects.select_related("organization")
            .values("partner_description", "organization__partner_program")
            .get(id=product_id)
        )

        return context

    def get_delete_product_popup(self, request):
        product_id = request.GET.get("product")
        context = dict()
        context["product"] = UserProduct.objects.values("id").get(id=product_id)

        return context

    def get_document_popup(self, request):
        document_slug = request.GET.get("document")

        return {"document": Document.objects.values("name", "text").get(slug=document_slug)}

    def get_create_idea_form(self, request):
        return {}


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor(get_referral_service(), get_products_service(), get_domain_service())
