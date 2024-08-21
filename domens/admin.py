from django.contrib import admin

from settings.models import Domain


class SiteAdmin(admin.ModelAdmin):
    exclude = ["online_from"]


class DomainAdmin(admin.ModelAdmin):
    pass


admin.site.register(Domain, DomainAdmin)
