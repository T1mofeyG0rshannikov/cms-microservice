import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from application.usecases.site.change_site import ChangeSite
from application.usecases.site.change_socials import ChangeSocials
from application.usecases.user.change_user import ChangeUser
from application.usecases.user_products.add_user_product import AddUserProduct
from domain.products.repository import ProductRepositoryInterface
from domain.user.exceptions import (
    SocialChannelAlreadyExists,
    UserProductAlreadyExists,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user_sessions.repository import UserSessionRepositoryInterface
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
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.add_session_action import IncrementSessionCount
from web.account.forms import (
    AddUserProductForm,
    ChangeSiteForm,
    ChangeSocialsForm,
    ChangeUserForm,
)
from web.common.views import FormView
from web.domens.exceptions import SiteAdressExists
from web.user.views.base_user_view import APIUserRequired


class ChangeSiteView(FormView, APIUserRequired):
    form_class = ChangeSiteForm
    domain_repository = get_domain_repository()
    change_site_interactor = ChangeSite(domain_repository)
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    increment_session_profile_action = IncrementSessionCount(
        get_user_session_repository(), settings.USER_ACTIVITY_SESSION_KEY, "profile_actions_count"
    )

    def form_valid(self, request: HttpRequest, form):
        user = request.user
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))
        site = self.domain_repository.get_user_site(user.id)

        if site:
            user_activity_text = f'''Изменил партнерский сайт "{site.subdomain}"'''
        else:
            user_activity_text = f'''Добавил партнерский сайт "{site.subdomain}"'''

        self.increment_session_profile_action(request.session)

        self.user_session_repository.create_user_action(
            adress=adress, text=user_activity_text, session_unique_key=request.session["user_activity"]["unique_key"]
        )

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
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    increment_session_profile_action = IncrementSessionCount(
        get_user_session_repository(), settings.USER_ACTIVITY_SESSION_KEY, "profile_actions_count"
    )

    def form_valid(self, request: HttpRequest, form):
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        try:
            email_changed = self.change_user_interactor(request.user, form.cleaned_data)

            self.increment_session_profile_action(request.session)
            self.user_session_repository.create_user_action(
                adress=adress,
                text="Изменил данные профиля",
                session_unique_key=request.session["user_activity"]["unique_key"],
            )

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
    product_repository: ProductRepositoryInterface = get_product_repository()
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    increment_session_profile_action = IncrementSessionCount(
        get_user_session_repository(), settings.USER_ACTIVITY_SESSION_KEY, "profile_actions_count"
    )

    def form_valid(self, request: HttpRequest, form):
        user = request.user

        try:
            self.add_user_product_interactor(form.cleaned_data, user)
        except UserProductAlreadyExists as e:
            return JsonResponse({"errors": str(e)}, status=400)

        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))

        product_id = int(request.POST.get("product"))

        product_name = self.product_repository.get_product_by_id(product_id).name
        user_product_exists = self.product_repository.user_product_exists(user_id=user.id, product_id=product_id)

        if user_product_exists:
            user_activity_text = f'''Изменил продукт "{product_name}"'''
        else:
            user_activity_text = f'''Добавил продукт "{product_name}"'''

        self.increment_session_profile_action(request.session)
        self.user_session_repository.create_user_action(
            adress=adress, text=user_activity_text, session_unique_key=request.session["user_activity"]["unique_key"]
        )

        return HttpResponse(status=200)
