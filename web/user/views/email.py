from django.http import HttpRequest, HttpResponseRedirect

from application.texts.errors import Errors
from domain.user.repository import UserRepositoryInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository
from web.user.views.base_user_view import BaseUserView


class ConfirmEmail(BaseUserView):
    user_repository: UserRepositoryInterface = get_user_repository()

    def get(self, request: HttpRequest, token: str) -> HttpResponseRedirect:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user = self.user_repository.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user.confirm_email()
        self.login(user)

        self.create_user_session_log(
            request=request,
            text=f"""Верифицировал емейл {user.email}""",
        )

        if not user.password:
            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return HttpResponseRedirect(f"/user/password/{token_to_set_password}")

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )


class ConfirmNewEmail(BaseUserView):
    user_repository: UserRepositoryInterface = get_user_repository()

    def get(self, request: HttpRequest, token) -> HttpResponseRedirect:
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user = self.user_repository.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link}")

        user.confirm_new_email()
        self.login(user)

        self.create_user_session_log(
            request=request,
            text=f"""Верифицировал емейл {user.email}""",
        )

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )
