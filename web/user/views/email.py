from django.http import HttpResponseRedirect

from application.texts.errors import Errors
from web.user.models.user import User
from web.user.views.base_user_view import BaseUserView


class ConfirmEmail(BaseUserView):
    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user = User.objects.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user.confirm_email()
        self.login(user)

        if not user.password:
            token_to_set_password = self.jwt_processor.create_set_password_token(user.id)

            return HttpResponseRedirect(f"/user/password/{token_to_set_password}")

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )


class ConfirmNewEmail(BaseUserView):
    def get(self, request, token):
        payload = self.jwt_processor.validate_token(token)

        if not payload:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user = User.objects.get_user_by_id(payload["user_id"])
        if user is None:
            return HttpResponseRedirect(f"/?error={Errors.wrong_confirm_email_link.value}")

        user.confirm_new_email()
        self.login(user)

        return HttpResponseRedirect(
            f"{self.account_url}?info_text={'Вы успешно подтвердили email адрес. Можно приступать к созданию вашего партнерского сайта.'}&info_title={'Email подтвержден'}"
        )
