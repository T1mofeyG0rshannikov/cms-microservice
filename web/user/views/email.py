from django.http import HttpRequest, HttpResponseRedirect

from application.common.base_url_parser import UrlParserInterface
from infrastructure.url_parser import get_url_parser
from application.texts.errors import Errors
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from web.user.views.base_user_view import BaseUserView


class ConfirmEmail(BaseUserView):
    user_repository: UserRepositoryInterface = get_user_repository()
    user_session_repository = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def get(self, request: HttpRequest, token):
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user = self.user_repository.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user.confirm_email()
        self.login(user)

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f"""Верифицировал емейл {user.email}""",
            session_id=request.user_session_id,
        )

        if not user.password:
            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return HttpResponseRedirect(f"/user/password/{token_to_set_password}")

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )


class ConfirmNewEmail(BaseUserView):
    user_repository: UserRepositoryInterface = get_user_repository()
    user_session_repository = get_user_session_repository()
    url_parser: UrlParserInterface = get_url_parser()

    def get(self, request: HttpRequest, token) -> HttpResponseRedirect:
        adress = self.url_parser.remove_protocol(request.META.get("HTTP_REFERER"))
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user = self.user_repository.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user.confirm_new_email()
        self.login(user)

        self.user_session_repository.create_user_action(
            adress=adress,
            text=f"""Верифицировал емейл {user.email}""",
            session_id=request.user_session_id,
        )

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )
