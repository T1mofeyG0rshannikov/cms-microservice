from typing import Any

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from application.texts.user_session import UserActions
from application.usecases.user.change_password import (
    ChangePassword,
    get_change_password_interactor,
)
from domain.materials.repository import DocumentRepositoryInterface
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
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.forms import ChangePasswordForm
from web.common.views import FormView
from web.domens.views.mixins import SubdomainMixin
from web.notifications.serializers import UserNotificationSerializer
from web.settings.views import SettingsMixin
from web.template.profile_template_loader.context_processor.context_processor import (
    get_profile_template_context_processor,
)
from web.template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from web.user.views.base_user_view import (
    APIUserRequired,
    BaseUserView,
    MyLoginRequiredMixin,
)


class BaseProfileView(MyLoginRequiredMixin, SubdomainMixin):
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()
    notifications_repository: NotificationRepositoryInterface = get_notification_repository()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["notifications"] = UserNotificationSerializer(
            self.notifications_repository.get_user_notifications(user_id=self.request.user.id),
            context={"user": self.request.user},
            many=True,
        ).data

        return context


class SiteView(BaseProfileView):
    template_name = "account/site.html"

    def get_context_data(self, **kwargs):
        return self.template_context_processor.get_site_template_context(self.request)


class RefsView(BaseProfileView):
    template_name = "account/refs.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            page_context = self.template_context_processor.get_refs_template_context(self.request)
            context |= page_context

        except (InvalidSortedByField, InvalidReferalLevel):
            pass

        return context


class ManualsView(BaseProfileView):
    template_name = "account/manuals.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs):
        return self.template_context_processor.get_manuals_template_context(self.request)


class ChangePasswordView(BaseUserView, FormView, APIUserRequired):
    form_class = ChangePasswordForm
    change_password_inteactor: ChangePassword = get_change_password_interactor()

    def form_valid(self, request: HttpRequest, form: ChangePasswordForm) -> JsonResponse:
        try:
            change_pass_response = self.change_password_inteactor(**form.cleaned_data, user=request.user)
            user = change_pass_response.user
            access_token = change_pass_response.access_token
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

        return JsonResponse({"access_token": access_token}, status=200)


class Profile(BaseProfileView, BaseUserView):
    template_name = "account/profile.html"

    def dispath(self, request: RequestInterface, *args, **kwargs):
        if request.user.is_authenticated():
            return super().dispatch(request, *args, **kwargs)
        if request.user_from_header:
            self.login(request.user_from_header)

        return super().dispatch(request, *args, **kwargs)


class PageNotFound(SubdomainMixin):
    template_name = "account/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


class DocumentPage(SettingsMixin):
    template_name = "account/manual.html"
    document_repository: DocumentRepositoryInterface = get_document_repository()

    def dispatch(self, request: HttpRequest, slug: str, *args, **kwargs):
        document = self.document_repository.get_document(slug)
        if not document:
            return PageNotFound.as_view()(request)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["document"] = self.document_repository.get_document(kwargs.get("slug"))

        return context


class UserProductsView(BaseProfileView):
    template_name = "account/products.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= self.template_context_processor.get_products_template_context(self.request)

        return context


class IdeasView(BaseProfileView):
    template_name = "account/ideas.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= self.template_context_processor.get_ideas_template_context(self.request)

        return context
