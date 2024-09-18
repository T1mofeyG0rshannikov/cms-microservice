import json

from account.forms import (
    AddUserProductForm,
    ChangeSiteForm,
    ChangeSocialsForm,
    ChangeUserForm,
)
from common.views import FormView
from django.http import HttpResponse, JsonResponse

from application.usecases.site.change_site import ChangeSite
from application.usecases.site.change_socials import ChangeSocials
from application.usecases.user.change_user import ChangeUser
from application.usecases.user_products.add_user_product import AddUserProduct
from domain.user.exceptions import (
    SocialChannelAlreadyExists,
    UserProductAlreadyExists,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)
from infrastructure.persistence.repositories.product_repository import (
    get_product_repository,
)
from infrastructure.persistence.repositories.socials_repositry import (
    get_socials_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from web.domens.exceptions import SiteAdressExists
from web.user.views.base_user_view import APIUserRequired


class ChangeSiteView(FormView, APIUserRequired):
    form_class = ChangeSiteForm
    change_site_interactor = ChangeSite(get_domain_repository())

    def form_valid(self, request, form):
        user = request.user

        try:
            self.change_site_interactor(form.cleaned_data, user_id=user.id)
        except SiteAdressExists as e:
            form.add_error("site", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        return HttpResponse(status=200)


class ChangeSocialsView(FormView, APIUserRequired):
    form_class = ChangeSocialsForm
    change_socials_interactor = ChangeSocials(get_socials_repository())

    def form_valid(self, request, form):
        try:
            user_social_networks = json.loads(form.cleaned_data.get("socials"))
            self.change_socials_interactor(request.user.site.id, user_social_networks)
        except SocialChannelAlreadyExists as e:
            form.add_error("socials", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        return HttpResponse(status=200)


class ChangeUserView(FormView, APIUserRequired):
    form_class = ChangeUserForm
    change_user_interactor = ChangeUser(get_user_repository())

    def form_valid(self, request, form):
        try:
            email_changed = self.change_user_interactor(request.user, form.cleaned_data)
            if email_changed:
                return JsonResponse(
                    {
                        "info": {
                            "title": "Вы меняете email",
                            "text": "На новый email адрес отправлено письмо со ссылкой для подтверждения",
                        }
                    },
                    status=202,
                )

        except UserWithEmailAlreadyExists as e:
            form.add_error("email", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        except UserWithPhoneAlreadyExists as e:
            form.add_error("phone", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        return HttpResponse(status=200)


class AddUserProductView(FormView, APIUserRequired):
    form_class = AddUserProductForm
    add_user_product_interactor = AddUserProduct(get_product_repository())

    def form_valid(self, request, form):
        user = request.user

        try:
            self.add_user_product_interactor(form.cleaned_data, user)
        except UserProductAlreadyExists as e:
            return JsonResponse({"errors": str(e)}, status=400)

        return HttpResponse(status=200)
