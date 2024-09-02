from django.db.models import Count, Q

from account.referrals_service.referrals_service import get_referral_service
from account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from account.serializers import ReferralsSerializer
from catalog.models.product_type import ProductCategory
from catalog.products_service.products_service import get_products_service
from catalog.products_service.products_service_interface import ProductsServiceInterface
from common.pagination import Pagination
from materials.models import Document
from template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from template.template_loader.tempate_context_processor.base_context_processor import (
    BaseContextProcessor,
)
from user.serializers import UserProductsSerializer


class ProfileTemplateContextProcessor(BaseContextProcessor, ProfileTemplateContextProcessorInterface):
    def __init__(self, referral_service: ReferralServiceInterface, products_service: ProductsServiceInterface):
        self.referral_service = referral_service
        self.products_service = products_service

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

    def get_products_template_context(self, request):
        context = self.get_context(request)

        context["product_categories"] = ProductCategory.objects.annotate(
            count=Count("products", filter=Q(products__user_products__user=request.user))
        ).filter(count__gte=1)

        product_category = request.GET.get("product_category")

        products = self.products_service.filter_user_products(category_id=product_category, user=request.user)

        pagination = Pagination(request)

        products = pagination.paginate(products, "products", UserProductsSerializer)
        context |= products

        return context


def get_profile_template_context_processor() -> ProfileTemplateContextProcessor:
    return ProfileTemplateContextProcessor(get_referral_service(), get_products_service())
