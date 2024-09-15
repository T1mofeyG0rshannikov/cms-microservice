from django.contrib import admin


class SiteAdmin(admin.ModelAdmin):
    exclude = ["online_from"]


class DomainAdmin(admin.ModelAdmin):
    pass
