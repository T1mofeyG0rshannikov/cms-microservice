from django.contrib import admin
from django.contrib.admin.decorators import register

from user.models import User

from .forms import CustomAuthenticationAdminForm


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "register_on", "email_is_confirmed"]
    exclude = ["password", "staff"]

    def register_on(self, obj):
        site = obj.register_on_site
        domain = obj.register_on_domain

        if site and domain:
            return ".".join([str(site), str(domain)])

        return ""

    register_on.short_description = "зарегистрирован на"
    register_on.allow_tags = True


admin.site.login_form = CustomAuthenticationAdminForm
