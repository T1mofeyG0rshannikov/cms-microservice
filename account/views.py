import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from account.forms import ChangePasswordForm, ChangeSiteForm, ChangeUserForm
from account.models import Messanger, UserFont, UserMessanger, UserSocialNetwork
from common.models import SocialNetwork
from common.views import SubdomainMixin
from domens.models import Site
from notifications.models import UserNotification
from notifications.serializers import UserNotificationSerializer
from settings.models import SiteSettings
from user.models import User
from user.views.base_user_view import BaseUserView, MyLoginRequiredMixin
from utils.errors import UserErrors


class BaseProfileView(MyLoginRequiredMixin, SubdomainMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["notifications"] = UserNotificationSerializer(
            UserNotification.objects.filter(user_id=self.request.user.id),
            context={"user": self.request.user},
            many=True,
        ).data

        context["messangers"] = Messanger.objects.select_related("social_network").all()
        context["fonts"] = UserFont.objects.all()
        context["socials"] = SocialNetwork.objects.all()

        context["default_user_size"] = SiteSettings.objects.values_list("default_users_font_size").first()[0]

        return context


class SiteView(BaseProfileView):
    template_name = "account/site.html"


@method_decorator(csrf_exempt, name="dispatch")
class ChangeSiteView(View):
    def post(self, request):
        user = request.user_from_header
        if user is None:
            return HttpResponse(status=401)

        print(request.POST)
        form = ChangeSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site_url = form.cleaned_data.get("site")
            if Site.objects.filter(user_id=user.id).exists():
                site = user.site
            else:
                site = Site.objects.create(
                    subdomain=form.cleaned_data["site"],
                    name=form.cleaned_data["name"],
                    owner=form.cleaned_data["owner"],
                    contact_info=form.cleaned_data["contact_info"],
                    font=UserFont.objects.get(id=form.cleaned_data["font"]),
                    font_size=form.cleaned_data["font_size"],
                    user=user,
                )

            if site.subdomain != site_url and Site.objects.filter(subdomain=site_url).exists():
                form.add_error("site", "Адрес занят")
                return JsonResponse({"errors": form.errors}, status=400)

            user_social_networks = json.loads(form.cleaned_data.get("socials"))
            social_networks_ids = [user_social_network["social"] for user_social_network in user_social_networks]

            if len({social_network["social"] for social_network in user_social_networks}) < len(user_social_networks):
                form.add_error("socials", "Вы можете указать только один канал для каждой соц. сети")
                return JsonResponse({"errors": form.errors}, status=400)

            all_social_networks = SocialNetwork.objects.all()

            for social_network in all_social_networks:
                if (
                    UserSocialNetwork.objects.filter(site=site, social_network=social_network).exists()
                    and social_network.id not in social_networks_ids
                ):
                    UserSocialNetwork.objects.filter(site=site, social_network=social_network).delete()

            if user_social_networks:
                for user_social_network in user_social_networks:
                    social_network = SocialNetwork(id=user_social_network["social"])

                    user_social_network, created = UserSocialNetwork.objects.update_or_create(
                        social_network=social_network,
                        site=site,
                        defaults={"adress": user_social_network["adress"]},
                    )

            site.subdomain = form.cleaned_data["site"]
            site.name = form.cleaned_data["name"]
            site.owner = form.cleaned_data["owner"]
            site.contact_info = form.cleaned_data["contact_info"]

            site.font = UserFont.objects.get(id=form.cleaned_data["font"])
            site.font_size = form.cleaned_data["font_size"]

            logo = form.cleaned_data.get("logo", None)
            if logo:
                site.logo = logo
                site.logo_width = int(260 * (form.cleaned_data["logo_width"] / 100))

            site.save()

            return HttpResponse(status=200)

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ChangeUserView(View):
    def post(self, request):
        if request.user_from_header is None:
            return HttpResponse(status=401)

        form = ChangeUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user_from_header

            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")

            user_with_phone = User.objects.get_user_by_phone(phone)
            user_with_email = User.objects.get_user_by_email(email)

            if user_with_email != user and user_with_email and user_with_email.email_is_confirmed:
                form.add_error("email", UserErrors.username_with_email_alredy_exists.value)

                return JsonResponse({"errors": form.errors}, status=400)

            elif user_with_phone != user and user_with_phone and user_with_phone.phone_is_confirmed:
                form.add_error("phone", UserErrors.username_with_phone_alredy_exists.value)

                return JsonResponse({"errors": form.errors}, status=400)

            user.username = form.cleaned_data.get("username")
            user.second_name = form.cleaned_data.get("second_name")

            user.email = form.cleaned_data.get("email")
            user.phone = form.cleaned_data.get("phone")

            if form.cleaned_data.get("social_network"):
                social_network = form.cleaned_data.get("social_network")
                adress = form.cleaned_data.get("adress")

                messanger = Messanger.objects.get(id=social_network)

                UserMessanger.objects.update_or_create(
                    user_id=user.id, defaults={"messanger": messanger, "adress": adress}
                )

            if form.cleaned_data.get("profile_picture"):
                user.profile_picture = form.cleaned_data.get("profile_picture")

            user.save()

            return HttpResponse(status=200)

        return JsonResponse({"errors": form.errors}, status=400)


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
    def get(self, request, template_name, **kwargs):
        context = self.get_context_data(**kwargs)

        content = loader.render_to_string(f"account/{template_name}.html", context, request, None)
        return JsonResponse({"content": content})
