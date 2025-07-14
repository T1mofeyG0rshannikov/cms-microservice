from typing import Any

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from application.texts.user_session import UserActions
from application.usecases.user.change_password import (
    ChangePassword,
    get_change_password_interactor,
)
from domain.page_blocks.settings_repository import SettingsRepositoryInterface
from infrastructure.persistence.repositories.settings_repository import get_settings_repository
from domain.materials.repository import DocumentRepositoryInterface
from domain.messanger.repository import MessangerRepositoryInterface
from domain.user.exceptions import (
    IncorrectPassword,
    InvalidPassword,
    InvalidReferalLevel,
    InvalidSortedByField,
)
from domain.user.notifications.repository import NotificationRepositoryInterface
from infrastructure.persistence.repositories.document_repository import (
    get_document_repository,
)
from infrastructure.persistence.repositories.messanger_repositroy import (
    get_messanger_repository,
)
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.forms import ChangePasswordForm
from web.common.views import FormView
from web.notifications.serializers import UserNotificationSerializer
from web.settings.views.settings_mixin import SettingsMixin
from web.styles.views import StylesMixin
from web.template.profile_template_loader.context_processor.context_processor import (
    get_profile_context_processor,
)
from web.template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from web.user.views.base_user_view import (
    APIUserRequired,
    BaseUserView,
    MyLoginRequiredMixin,
)


class BaseProfileView(MyLoginRequiredMixin, SettingsMixin, StylesMixin):
    context_processor: ProfileTemplateContextProcessorInterface = get_profile_context_processor()
    notifications_repository: NotificationRepositoryInterface = get_notification_repository()
    messanger_repository: MessangerRepositoryInterface = get_messanger_repository()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | self.get_styles_context()
        user = self.request.user

        context["notifications"] = UserNotificationSerializer(
            self.notifications_repository.get_notifications(user_id=user.id),
            context={"user": user},
            many=True,
        ).data

        context["unreaden_messages_count"] = self.messanger_repository.count_unreadable(user_id=user.id)

        return context


class SiteView(BaseProfileView):
    template_name = "account/site.html"

    def get_context_data(self, **kwargs):
        settings_repository: SettingsRepositoryInterface = get_settings_repository()

        return super().get_context_data(**kwargs) | self.context_processor.get_site_context(self.request)


class RefsView(BaseProfileView):
    template_name = "account/refs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            page_context = self.context_processor.get_refs_context(self.request)
            context |= page_context

        except (InvalidSortedByField, InvalidReferalLevel):
            pass

        return context


class ManualsView(BaseProfileView):
    template_name = "account/manuals.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.context_processor.get_manuals_context(self.request)


class ChangePasswordView(BaseUserView, FormView, APIUserRequired):
    form_class = ChangePasswordForm
    inteactor: ChangePassword = get_change_password_interactor()

    def form_valid(self, request: HttpRequest, form: ChangePasswordForm) -> JsonResponse:
        try:
            response = self.inteactor(**form.cleaned_data, user=request.user)
            user = response.user
        except IncorrectPassword as e:
            form.add_error("current_password", str(e))
            return JsonResponse({"errors": form.errors}, status=400)
        except InvalidPassword as e:
            form.add_error("password", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        request.user = user
        user = authenticate(request)
        login(request, user)

        self.create_user_session_log(request=request, text=UserActions.changed_password)

        return JsonResponse({
            "access_token": response.access_token,
            "refresh_token": response.refresh_token
        }, status=200)


class Profile(BaseProfileView, BaseUserView):
    template_name = "account/profile.html"

    def dispath(self, request: RequestInterface, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if request.user_from_header:
            self.login(request.user_from_header)

        return super().dispatch(request, *args, **kwargs)


class PageNotFound(SettingsMixin):
    template_name = "account/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


class DocumentPage(SettingsMixin):
    template_name = "account/manual.html"
    document_repository: DocumentRepositoryInterface = get_document_repository()

    def dispatch(self, request: HttpRequest, slug: str, *args, **kwargs):
        document = self.document_repository.get(slug)
        if not document:
            return PageNotFound.as_view()(request)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, slug: str, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["document"] = self.document_repository.get(slug)

        return context


class UserProductsView(BaseProfileView):
    template_name = "account/products.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= self.context_processor.get_products_context(self.request)

        return context


class IdeasView(BaseProfileView):
    template_name = "account/ideas.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= self.context_processor.get_ideas_context(self.request)

        return context


class MessangerView(BaseProfileView):
    template_name = "account/messanger.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= self.context_processor.get_messanger_context(self.request)

        return context
