from django.db.models import Count, Q

from account.models import Messanger
from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from catalog.models.products import Organization, Product
from catalog.products_service.products_service import get_products_service
from catalog.serializers import ProductSerializer, ProductsSerializer
from domens.domain_service.domain_service import DomainService
from settings.models import Domain, SiteSettings, SocialNetwork, UserFont
from template.template_loader.tempate_context_processor.base_context_processor import (
    BaseContextProcessor,
)

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(BaseContextProcessor, TemplateContextProcessorInterface):
    def __init__(self, referral_service: ReferralServiceInterface, products_service):
        self.referral_service = referral_service
        self.products_service = products_service

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
        context["organizations"] = (
            Organization.objects.annotate(
                count=Count("products", filter=Q(products__status="Опубликовано")),
                user_products_count=Count("products", filter=Q(products__user_products__user=request.user)),
            )
            .values("name", "id")
            .filter(count__gte=1, user_products_count__lte=0)
            .order_by("name")
        )

        products = self.products_service.get_enabled_products_to_create(request.user)

        context["products"] = ProductsSerializer(products, many=True).data

        return context

    def get_create_user_product_form(self, request):
        context = self.get_context(request)
        context["site_name"] = DomainService.get_site_name()

        product_id = request.GET.get("product")
        try:
            product = Product.objects.get(id=product_id)
            context["product"] = ProductSerializer(product).data

        except Product.DoesNotExist:
            pass

        return context


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor(get_referral_service(), get_products_service())
