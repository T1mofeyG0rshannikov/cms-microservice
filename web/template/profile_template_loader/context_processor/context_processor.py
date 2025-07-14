from typing import Any

from django.http import HttpRequest

from application.services.messanger_service import get_messanger_service
from application.services.user.referrals_service import get_referral_service
from application.usecases.ideas.get_ideas import GetIdeas, get_get_ideas_interactor
from application.mappers.site import from_orm_to_site
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.repositories.settings_repository import get_settings_repository
from domain.domains.domain_repository import DomainRepositoryInterface
from domain.materials.repository import DocumentRepositoryInterface
from domain.products.repository import ProductRepositoryInterface
from domain.referrals.service import ReferralServiceInterface
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.persistence.repositories.document_repository import (
    get_document_repository,
)
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)
from web.account.serializers import ReferralsSerializer
from web.common.pagination import Pagination
from web.messanger.get_context import get_chat_body_context
from web.messanger.serializers import ChatInterlocutorSerializer, MesageSerializer
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
        product_repository: ProductRepositoryInterface,
        user_product_repository: UserProductRepositoryInterface,
        domain_repository: DomainRepositoryInterface,
        get_ideas_interactor: GetIdeas,
    ):
        self.domain_repository = domain_repository
        self.referral_service = referral_service
        self.product_repository = product_repository
        self.user_product_repository = user_product_repository
        self.get_ideas_interactor = get_ideas_interactor

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        context = super().get_context(request)
        context["site_name"] = self.domain_repository.get_site_name()

        return context

    def get_profile_context(self, request: HttpRequest):
        return self.get_context(request)

    def get_site_context(self, request: HttpRequest, settings_repository: SettingsRepositoryInterface = get_settings_repository()):
        context = self.get_context(request)
        site = request.user.site

        if site:
            site = from_orm_to_site(site)

        context["site"] = site
        
        context["fonts"] = settings_repository.get_user_fonts()
        context["default_user_size"] = settings_repository.get_settings().default_users_font_size
        context["domains"] = settings_repository.get_partner_domains()

        return context

    def get_refs_context(self, request: HttpRequest):
        context = self.get_context(request)

        level = request.GET.get("level")
        sorted_by = request.GET.get("sorted_by", "created_at")

        pagination = Pagination(request)

        referrals = pagination.paginate(
            self.referral_service.get_referrals(level=level, user_id=request.user.id, sorted_by=sorted_by),
            "referrals",
            ReferralsSerializer,
        )

        context |= referrals

        return context

    def get_manuals_context(
        self, request: HttpRequest, document_repository: DocumentRepositoryInterface = get_document_repository()
    ):
        context = self.get_context(request)
        context["manuals"] = document_repository.all()

        return context

    def get_ideas_context(self, request: HttpRequest) -> dict[str, Any]:
        context = self.get_context(request)
        filter = request.GET.get("filter")
        sorted_by = request.GET.get("sorted_by")
        status = request.GET.get("status")

        ideas = self.get_ideas_interactor(filter=filter, sorted_by=sorted_by, status=status, user_id=request.user.id)

        pagination = Pagination(request)

        context |= pagination.paginate(ideas, "ideas", IdeasSerializer, {"user": request.user})

        return context

    def get_products_context(self, request: HttpRequest):
        context = self.get_context(request)

        context["product_categories"] = self.product_repository.get_product_categories(request.user.id)

        product_category = request.GET.get("product_category")

        pagination = Pagination(request)

        products = pagination.paginate(
            self.user_product_repository.filter(category_id=product_category, user_id=request.user.id),
            "products",
            UserProductsSerializer,
        )

        context |= products

        return context

    def get_messanger_context(self, request: HttpRequest, messanger_service=get_messanger_service()):
        context = self.get_context(request)
        user = request.user
        chats = messanger_service.get_chats(user)
        serialized_chats = []

        for chat in chats:
            serialized_chats.append(
                {
                    "chatuser": ChatInterlocutorSerializer(chat["chat_user"]).data,
                    "message": MesageSerializer(chat["message"]).data,
                }
            )

        chat_id = request.GET.get("chat_id")
        if chat_id:
            context |= get_chat_body_context(request)

        context["chats"] = serialized_chats
        return context


def get_profile_context_processor(
    referral_service: ReferralServiceInterface = get_referral_service(),
    product_repository: ProductRepositoryInterface = get_product_repository(),
    domain_repositrory: DomainRepositoryInterface = get_domain_repository(),
    user_product_repository: UserProductRepositoryInterface = get_user_product_repository(),
    get_ideas_interactor: GetIdeas = get_get_ideas_interactor(),
) -> ProfileTemplateContextProcessorInterface:
    return ProfileTemplateContextProcessor(
        referral_service=referral_service,
        product_repository=product_repository,
        domain_repository=domain_repositrory,
        user_product_repository=user_product_repository,
        get_ideas_interactor=get_ideas_interactor,
    )
