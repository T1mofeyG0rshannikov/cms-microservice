from django.contrib import admin
from django.contrib.admin import AdminSite

from common.models import SocialNetwork
from user.forms import CustomAuthenticationAdminForm


class BaseInline(admin.StackedInline):
    extra = 0


class SocialNetworkAdmin(admin.ModelAdmin):
    pass


class MyAdminSite(AdminSite):
    site_header = "Bankomag"
    index_title = "bankomag"
    login_form = CustomAuthenticationAdminForm

    def get_app_list(self, request, app_label=None):
        app_order = ["user", "catalog", "blocks", "account", "domens", "common", "settings"]
        app_order_dict = dict(zip(app_order, range(len(app_order))))
        app_list = list(self._build_app_dict(request).values())
        app_list.sort(key=lambda x: app_order_dict.get(x["app_label"], 0))

        return app_list


admin.site = MyAdminSite()
admin.site.register(SocialNetwork, SocialNetworkAdmin)
