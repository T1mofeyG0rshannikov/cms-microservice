from user.models import User
from django.contrib.auth.backends import ModelBackend


class CustomAdminAuthentication(ModelBackend):
    def authenticate(self, request):
        print(request.user, "3")
        return request.user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None