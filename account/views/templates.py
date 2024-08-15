from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from account.forms import ChangePasswordForm
from common.pagination import Pagination
from domens.views.mixins import SubdomainMixin
from notifications.models import UserNotification
from notifications.serializers import UserNotificationSerializer
from user.exceptions import InvalidReferalLevel, InvalidSortedByField
from user.user_service.user_service import get_user_service
from user.user_service.user_service_interface import UserServiceInterface
from user.views.base_user_view import BaseUserView, MyLoginRequiredMixin


class BaseProfileView(MyLoginRequiredMixin, SubdomainMixin):
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


class RefsView(BaseProfileView):
    template_name = "account/refs.html"
    user_service: UserServiceInterface = get_user_service()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        level = self.request.GET.get("level")
        sorted_by = self.request.GET.get("sorted_by")

        try:
            referrals = self.user_service.get_referrals(level=level, user=self.request.user, sorted_by=sorted_by)
        except InvalidSortedByField as e:
            return JsonResponse({"error": str(e)}, status=400)
        except InvalidReferalLevel as e:
            return JsonResponse({"error": str(e)}, status=400)

        pagination = Pagination(self.request)

        referrals = pagination.paginate(referrals, "referrals")

        context = {**context, **referrals}

        return context


@method_decorator(csrf_exempt, name="dispatch")
class ChangePasswordView(BaseUserView):
    def post(self, request):
        print(request.POST)

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
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

        return JsonResponse({"errors": form.errors}, status=400)


class Profile(BaseProfileView):
    template_name = "account/profile.html"


class ProfileTemplate(BaseProfileView):
    user_service = get_user_service()

    def get(self, request, template_name, **kwargs):
        context = self.get_context_data(**kwargs)

        if template_name == "refs-content":
            level = self.request.GET.get("level")
            sorted_by = self.request.GET.get("sorted_by")

            try:
                referrals = self.user_service.get_referrals(level=level, user=self.request.user, sorted_by=sorted_by)
            except InvalidSortedByField as e:
                return JsonResponse({"error": str(e)}, status=400)
            except InvalidReferalLevel as e:
                return JsonResponse({"error": str(e)}, status=400)

            pagination = Pagination(request)

            referrals = pagination.paginate(referrals, "referrals")
            context = {**context, **referrals}

        content = loader.render_to_string(f"account/{template_name}.html", context, request, None)
        return JsonResponse({"content": content})


class PageNotFound(SubdomainMixin):
    template_name = "account/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(), status=404)
