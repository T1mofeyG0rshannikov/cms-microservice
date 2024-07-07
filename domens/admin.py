from django.contrib import admin

from domens.models import Domain, Site


class SiteAdmin(admin.ModelAdmin):
    exclude = ["online_from"]


class DomainAdmin(admin.ModelAdmin):
    pass


admin.site.register(Site, SiteAdmin)
admin.site.register(Domain, DomainAdmin)
