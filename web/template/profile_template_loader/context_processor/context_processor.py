from django.db.models import Count, Q

from application.services.domains.service import get_domain_service
from application.usecases.ideas.get_ideas import GetIdeas
from domain.domains.interfaces.domain_service_interface import DomainServiceInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository
from web.account.referrals_service.referrals_service import get_referral_service
from web.account.referrals_service.referrals_service_interface import (
    ReferralServiceInterface,
)
from web.account.serializers import ReferralsSerializer
from web.catalog.models.product_type import ProductCategory
from web.catalog.products_service.products_service import get_products_service
from web.catalog.products_service.products_service_interface import (
    ProductsServiceInterface,
)
from web.common.pagination import Pagination
from web.materials.models import Document
from web.template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from web.template.template_loader.tempate_context_processor.base_context_processor import (
    BaseContextProcessor,
)
from web.user.serializers import IdeasSerializer, UserProductsSerializer


class ProfileTemplateContextProcessor(BaseContextProcessor, ProfileTemplateContextProcessorInterface):
    def __init__(
        self,
        referral_service: ReferralServiceInterface,
        products_service: ProductsServiceInterface,
        domain_service: DomainServiceInterface,
        get_ideas_interactor,
    ):
        self.referral_service = referral_service
        self.products_service = products_service
        self.domain_service = domain_service
        self.get_ideas_interactor = get_ideas_interactor

    def get_context(self, request):
        context = super().get_context(request)
        context["site_name"] = self.domain_service.get_site_name()

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

        context |= referrals

        return context

    def get_manuals_template_context(self, request):
        context = self.get_context(request)
        context["manuals"] = Document.objects.values("title", "slug").all()

        return context

    def get_ideas_template_context(self, request):
        context = self.get_context(request)
        filter = request.GET.get("filter")
        sorted_by = request.GET.get("sorted_by")
        status = request.GET.get("status")

        ideas = self.get_ideas_interactor(filter=filter, sorted_by=sorted_by, status=status, user=request.user)

        pagination = Pagination(request)

        context |= pagination.paginate(ideas, "ideas", IdeasSerializer, {"user": request.user})

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
    return ProfileTemplateContextProcessor(
        get_referral_service(), get_products_service(), get_domain_service(), GetIdeas(get_idea_repository())
    )
