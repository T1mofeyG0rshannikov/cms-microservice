from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import mark_safe

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

    def image_tag(self, screen):
        return mark_safe(
            '<a href="#" class="open-image-popup" data-image="%s"><img src="%s" width="100" /></a>'
            % (screen.screen.url, screen.screen.url)
        )

    image_tag.allow_tags = True
    image_tag.short_description = "Скрин"

    fields = ["image_tag"]
    readonly_fields = ["image_tag"]


class IdeaAdmin(admin.ModelAdmin):
    model = Idea
    list_display = ["status_img", "created_at_tag", "title", "user", "status", "finishe_date_tag", "rating"]

    def finishe_date_tag(self, idea):
        if idea.finishe_date:
            return idea.finishe_date.strftime("%d.%m.%Y")

        return "---"

    def created_at_tag(self, idea):
        return idea.created_at.strftime("%d.%m.%Y")

    def status_img(self, idea):
        if idea.category == "errors":
            src = "/static/account/images/bugs/icobug_error.png"
        elif idea.category == "correction":
            src = "/static/account/images/bugs/icobug_fix.png"
        elif idea.category == "modernization":
            src = "/static/account/images/bugs/icobug_addon.png"
        elif idea.category == "new_feature":
            src = "/static/account/images/bugs/icobug_idea.png"

        return mark_safe(f'<img width="15" src="{src}" />')

    status_img.short_description = ""
    created_at_tag.short_description = "Дата"
    finishe_date_tag.short_description = "Срок"

    readonly_fields = ["user", "title", "description", "rating"]

    change_form_template = "common/screen_inline.html"

    def rating(self, idea):
        return idea.likes.count()

    rating.short_description = "Рейтинг"

    inlines = [IdeaScreenInline]


admin.site = MyAdminSite()
admin.site.register(User, UserAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(UserProduct)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Like)
