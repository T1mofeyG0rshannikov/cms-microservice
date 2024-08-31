from django.db.models import Count, Q

from account.models import Messanger
from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralsSerializer
from catalog.models.product_type import ProductCategory
from catalog.models.products import Organization, Product
from catalog.products_service.products_service import get_products_service
from catalog.serializers import ProductSerializer, ProductsSerializer
from common.pagination import Pagination
from domens.domain_service.domain_service import DomainService
from materials.models import Document
from settings.models import Domain, SiteSettings, SocialNetwork, UserFont
from user.serializers import UserProductsSerializer

from .template_context_processor_interface import TemplateContextProcessorInterface


class TemplateContextProcessor(TemplateContextProcessorInterface):
    def __init__(self, referral_service: ReferralServiceInterface, products_service):
        self.referral_service = referral_service
        self.products_service = products_service

    @staticmethod
    def get_context(request):
        context = {"request": request, "user": request.user}
        return context

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

    def get_profile_template_context(self, request):
        context = self.get_context(request)

        return context

    def get_site_template_context(self, request):
        context = self.get_context(request)

        return context

    def get_refs_template_context(self, request):
        context = self.get_context(request)

        level = request.GET.get("level")
        sorted_by = request.GET.get("sorted_by")

        referrals = self.referral_service.get_referrals(level=level, user=request.user, sorted_by=sorted_by)

        pagination = Pagination(request)

        referrals = pagination.paginate(referrals, "referrals", ReferralsSerializer)

        context = {**context, **referrals}

        return context

    def get_manuals_template_context(self, request):
        context = self.get_context(request)

        context["manuals"] = Document.objects.values("title", "slug").all()

        return context

    def get_choice_product_form(self, request):
        context = self.get_context(request)
        context["organizations"] = (
            Organization.objects.annotate(
                count=Count("products"),
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

    def get_products_template_context(self, request):
        context = self.get_context(request)
        product_categories = ProductCategory.objects.annotate(
            count=Count("products", filter=Q(products__user_products__user=request.user))
        ).filter(count__gte=1)
        context["product_categories"] = product_categories

        product_category = request.GET.get("product_category")

        products = self.products_service.filter_user_products(category_id=product_category, user=request.user)

        pagination = Pagination(request)

        products = pagination.paginate(products, "products", UserProductsSerializer)
        context |= products

        return context


def get_template_context_processor() -> TemplateContextProcessor:
    return TemplateContextProcessor(get_referral_service(), get_products_service())
