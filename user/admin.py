from django.contrib import admin

from domens.domain_service.domain_service import get_domain_service


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "register_on", "email_is_confirmed"]
    exclude = ["password", "staff", "is_superuser"]

    def register_on(self, obj):
        domain_service = get_domain_service()
        return domain_service.get_register_on_site(obj)

    register_on.short_description = "зарегистрирован на"
    register_on.allow_tags = True
