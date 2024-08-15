from django.contrib import admin
from django.contrib.admin.decorators import register

from domens.domain_service.domain_service import DomainService
from user.models import User

from .forms import CustomAuthenticationAdminForm


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "register_on", "email_is_confirmed"]
    exclude = ["password", "staff"]

    def register_on(self, obj):
        domain_service = DomainService()
        return domain_service.get_register_on_site(obj)

    register_on.short_description = "зарегистрирован на"
    register_on.allow_tags = True


admin.site.login_form = CustomAuthenticationAdminForm
