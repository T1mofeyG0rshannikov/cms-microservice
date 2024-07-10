import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from account.forms import ChangePasswordForm, ChangeSiteForm, ChangeUserForm
from account.models import UserFont, UserSocialNetwork
from common.models import SocialNetwork
from domens.models import Site
from user.views.base_user_view import MyLoginRequiredMixin


class SiteView(TemplateView, MyLoginRequiredMixin):
    template_name = "account/site.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["socials"] = SocialNetwork.objects.all()
        context["fonts"] = UserFont.objects.all()

        return context


@method_decorator(csrf_exempt, name="dispatch")
class ChangeSiteView(View):
    def post(self, request):
        print(request.POST)
        form = ChangeSiteForm(request.POST)
        if form.is_valid():
            site_url = form.cleaned_data.get("site")
            user = request.user_from_header
            site = user.site

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
        print(request.POST)
        print(request.FILES)
        form = ChangeUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["profile_picture"])
            print("success")

            return HttpResponse(status=200)

        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ChangePasswordView(View):
    def post(self, request):
        print(request.POST)

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user_from_header
            print(user)

            if not user.check_password(form.cleaned_data.get("current_password")):
                form.add_error("current_password", "неверный пароль")
                return JsonResponse({"errors": form.errors}, status=400)

            password = form.cleaned_data.get("password")
            repeat_password = form.cleaned_data.get("repeat_password")

            if password != repeat_password:
                form.add_error("password", "пароли не совпадают")
                return JsonResponse({"errors": form.errors}, status=400)

            user.set_password(password)
            user.save()

            return HttpResponse(status=200)

        return JsonResponse({"errors": form.errors}, status=400)
