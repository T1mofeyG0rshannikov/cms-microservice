import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from application.sessions.add_session_action import (
    IncrementSessionCount,
    get_increment_session_count,
)
from application.texts.user_session import UserActions
from application.usecases.site.change_site import ChangeSite, get_change_site_interactor
from application.usecases.site.change_socials import (
    ChangeSocials,
    get_change_socials_interactor,
)
from application.usecases.user.change_user import ChangeUser, get_change_user_interactor
from application.usecases.user_products.add_user_product import (
    AddUserProduct,
    get_add_product_interactor,
)
from domain.common.exceptons import InvalidFileExtension, ToLagreFile, ToLargeImageSize
from domain.user.exceptions import (
    LinkOrConnectedRequired,
    SocialChannelAlreadyExists,
    UserProductAlreadyExists,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.sites.exceptions import (
    InvalidSiteAddress,
    InvalidSiteName,
    SiteAdressExists,
)
from domain.user.user_product_repository import UserProductRepositoryInterface
from infrastructure.logging.user_activity.create_session_log import (
    CreateUserSesssionLog,
    get_create_user_session_log,
)
from infrastructure.persistence.repositories.user_product_repository import (
    get_user_product_repository,
)
from infrastructure.requests.request_interface import RequestInterface
from web.account.forms import (
    AddUserProductForm,
    ChangeSiteForm,
    ChangeSocialsForm,
    ChangeUserForm,
)
from web.common.views import FormView
from web.user.views.base_user_view import APIUserRequired


class ChangeSiteView(FormView, APIUserRequired):
    form_class = ChangeSiteForm
    change_site_interactor: ChangeSite = get_change_site_interactor()
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")

    def form_valid(self, request: HttpRequest, form: ChangeSiteForm) -> HttpResponse:
        user = request.user

        try:
            site, created = self.change_site_interactor(**form.cleaned_data, user_id=user.id)
        except (SiteAdressExists, InvalidSiteAddress) as e:
            form.add_error("subdomain", str(e))
            return JsonResponse({"errors": form.errors}, status=400)
        except InvalidSiteName as e:
            form.add_error("name", str(e))
            return JsonResponse({"errors": form.errors}, status=400)
        except (ToLagreFile, ToLargeImageSize, InvalidFileExtension) as e:
            form.add_error("name", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        if created:
            user_activity_text = f'''Добавил партнерский сайт "{site.subdomain}"'''
        else:
            user_activity_text = f'''Изменил партнерский сайт "{site.subdomain}"'''

        self.increment_session_profile_action(request)

        self.create_user_session_log(request=request, text=user_activity_text)

        return HttpResponse(status=200)


class ChangeSocialsView(FormView, APIUserRequired):
    form_class = ChangeSocialsForm
    change_socials_interactor: ChangeSocials = get_change_socials_interactor()

    def form_valid(self, request: RequestInterface, form: ChangeSocialsForm) -> HttpResponse:
        try:
            user_social_networks = json.loads(form.cleaned_data.get("socials"))

            self.change_socials_interactor(request.user.site.id, user_social_networks)
        except SocialChannelAlreadyExists as e:
            form.add_error("socials", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        return HttpResponse(status=200)


class ChangeUserView(FormView, APIUserRequired):
    form_class = ChangeUserForm
    change_user_interactor: ChangeUser = get_change_user_interactor()
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def form_valid(self, request: HttpRequest, form: ChangeUserForm) -> HttpResponse:
        try:
            email_changed = self.change_user_interactor(request.user, **form.cleaned_data).changed_email

            self.increment_session_profile_action(request=request, text=UserActions.changed_profile_data)
            self.create_user_session_log(request=request, text=UserActions.changed_profile_data)

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
    add_user_product_interactor: AddUserProduct = get_add_product_interactor()
    user_product_repository: UserProductRepositoryInterface = get_user_product_repository()
    increment_session_profile_action: IncrementSessionCount = get_increment_session_count("profile_actions_count")
    create_user_session_log: CreateUserSesssionLog = get_create_user_session_log()

    def form_valid(self, request: HttpRequest, form: AddUserProductForm) -> HttpResponse:
        user = request.user

        try:
            user_product, created = self.add_user_product_interactor(user_id=user.id, **form.cleaned_data)
        except UserProductAlreadyExists as e:
            return JsonResponse({"errors": str(e)}, status=400)
        except LinkOrConnectedRequired as e:
            form.add_error("link", str(e))
            return JsonResponse({"errors": form.errors}, status=400)

        product_name = user_product.product.name
        user_product_exists = self.user_product_repository.exists(user_id=user.id, product_id=user_product.product_id)

        user_activity_text = (
            f'''Изменил продукт "{product_name}"''' if user_product_exists else f'''Добавил продукт "{product_name}"'''
        )

        self.increment_session_profile_action(request=request)
        self.create_user_session_log(request=request, text=user_activity_text)

        return HttpResponse(status=200)
