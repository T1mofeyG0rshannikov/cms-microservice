from django.contrib.auth.backends import ModelBackend

from user.models import User


class CustomAdminAuthentication(ModelBackend):
    def authenticate(self, request):
        return request.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
