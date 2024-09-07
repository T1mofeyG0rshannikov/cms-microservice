from django.contrib import admin
from django.contrib.admin import AdminSite

from domens.admin import SiteAdmin
from user.admin import UserAdmin
from user.forms import CustomAuthenticationAdminForm
from user.models.idea import Idea, IdeaScreen, Like
from user.models.product import UserProduct
from user.models.site import Site
from user.models.user import User


class BaseInline(admin.StackedInline):
    extra = 0


class SocialNetworkAdmin(admin.ModelAdmin):
    pass


class MyAdminSite(AdminSite):
    site_header = "Bankomag"
    index_title = "bankomag"
    login_form = CustomAuthenticationAdminForm

    def get_app_list(self, request, app_label=None):
        app_order = [
            "user",
            "catalog",
            "materials",
            "blocks",
            "settings",
            "notifications",
            "account",
            "domens",
            "common",
            "styles",
            "site_tests",
        ]
        app_order_dict = dict(zip(app_order, range(len(app_order))))
        app_list = list(self._build_app_dict(request).values())
        app_list.sort(key=lambda x: app_order_dict.get(x["app_label"], 0))

        return app_list


class IdeaScreenInline(BaseInline):
    model = IdeaScreen


class IdeaAdmin(admin.ModelAdmin):
    model = Idea
    inlines = [IdeaScreenInline]


admin.site = MyAdminSite()
admin.site.register(User, UserAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(UserProduct)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Like)
