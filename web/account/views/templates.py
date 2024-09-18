from account.forms import ChangePasswordForm
from common.views import FormView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from domens.views.mixins import SubdomainMixin
from settings.views import SettingsMixin

from domain.user.exceptions import InvalidReferalLevel, InvalidSortedByField
from web.materials.models import Document
from web.notifications.models import UserNotification
from web.notifications.serializers import UserNotificationSerializer
from web.template.profile_template_loader.context_processor.context_processor import (
    get_profile_template_context_processor,
)
from web.template.profile_template_loader.context_processor.context_processor_interface import (
    ProfileTemplateContextProcessorInterface,
)
from web.user.views.base_user_view import BaseUserView, MyLoginRequiredMixin


class BaseProfileView(MyLoginRequiredMixin, SubdomainMixin):
    template_context_processor = get_profile_template_context_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["notifications"] = UserNotificationSerializer(
            UserNotification.objects.filter(user_id=self.request.user.id),
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


@method_decorator(csrf_exempt, name="dispatch")
class ChangePasswordView(BaseUserView, FormView):
    form_class = ChangePasswordForm

    def form_valid(self, request, form):
        user = request.user_from_header

        if not user.check_password(form.cleaned_data.get("current_password")):
            form.add_error("current_password", "Неверный пароль")
            return JsonResponse({"errors": form.errors}, status=400)

        password = form.cleaned_data.get("password")
        repeat_password = form.cleaned_data.get("repeat_password")

        if password != repeat_password:
            form.add_error("password", "Пароли не совпадают")
            return JsonResponse({"errors": form.errors}, status=400)

        user.set_password(password)
        user.save()

        request.user = user
        user = authenticate(request)
        login(request, user)

        access_token = self.jwt_processor.create_access_token(user.username, user.id)

        return JsonResponse({"access_token": access_token}, status=200)


class Profile(BaseProfileView):
    template_name = "account/profile.html"


class PageNotFound(SubdomainMixin):
    template_name = "account/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)


class DocumentPage(SettingsMixin):
    template_name = "account/manual.html"

    def dispatch(self, request, slug, *args, **kwargs):
        try:
            Document.objects.get(slug=slug)
        except Document.DoesNotExist:
            return PageNotFound.as_view()(request)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["document"] = Document.objects.get(slug=self.kwargs.get("slug"))

        return context


class UserProductsView(BaseProfileView):
    template_name = "account/products.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.template_context_processor.get_products_template_context(self.request)

        return context


class IdeasView(BaseProfileView):
    template_name = "account/ideas.html"
    template_context_processor: ProfileTemplateContextProcessorInterface = get_profile_template_context_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.template_context_processor.get_ideas_template_context(self.request)

        return context
