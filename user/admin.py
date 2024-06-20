from django.contrib import admin
from django.contrib.admin.decorators import register

from user.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "email_is_confirmed"]

from django.contrib import admin
from django.contrib.auth.views import LoginView
from user.views.views import Login#, AdminLogin
from .forms import CustomAuthenticationAdminForm
'''
class CustomLoginView(View):
    template_name = "user/admin_login.html"
    authentication_form = CustomAuthenticationAdminForm
'''
admin.site.login_form = CustomAuthenticationAdminForm



from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from user.user_manager.user_manager import get_user_manager

'''
class SettingsBackend(BaseBackend):
    def __init__(self):
        self.user_manager = get_user_manager()
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, phone_or_email: str, password=None):
        user1 = self.user_manager.get_user_by_email(phone_or_email)
        user2 = self.user_manager.get_user_by_phone(phone_or_email)
        
        if user1:
            return user1
        
        if user2:
            return user2
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
'''