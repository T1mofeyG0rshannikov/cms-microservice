from django.contrib import admin


class BaseInline(admin.StackedInline):
    extra = 0


class SocialNetworkAdmin(admin.ModelAdmin):
    pass
