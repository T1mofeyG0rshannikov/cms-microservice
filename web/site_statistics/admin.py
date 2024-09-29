from django.conf import settings
from django.contrib import admin
from django.utils.html import mark_safe

from infrastructure.admin.admin_settings import get_admin_settings
from web.admin.admin import redirect_to_change_page_tag
from web.common.admin import BaseInline
from web.site_statistics.models import (
    SessionAction,
    SessionFilters,
    SessionModel,
    TryLoginToAdminPanel,
    TryLoginToFakeAdminPanel,
    UserAction,
    UserActivity,
)


class UserActionInline(BaseInline):
    model = UserAction
    fields = ["action"]
    readonly_fields = fields

    def action(self, obj):
        return f"""{obj.time.strftime('%d.%m %H:%M:%S')}:{r"     "}{obj.adress} - {obj.text}"""

    action.short_description = ""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False


class BaseSessionAdmin(admin.ModelAdmin):
    admin_url = get_admin_settings().admin_url

    def start_time_tag(self, obj):
        return obj.start_time.strftime("%d.%m %H:%M:%S")

    start_time_tag.short_description = "Дата"

    def time_tag(self, obj):
        return str(obj.end_time - obj.start_time).split(".")[0]

    time_tag.short_description = "Время"

    def device_tag(self, obj):
        src = f"""{settings.STATIC_URL}site_statistics/images/{"icoadm_desktop.png" if not obj.device else "icoadm_smart.png"}"""

        return mark_safe(f"""<img height="15" src={src} />""")

    device_tag.short_description = ""

    def ip_tag(self, obj):
        return redirect_to_change_page_tag(obj, obj.ip)

    ip_tag.short_description = "ip"

    class Media:
        css = {"all": ("site_statistics/css/user_action_admin.css",)}


class UserActivityAdmin(BaseSessionAdmin):
    inlines = [UserActionInline]

    fields = [
        "device_tag",
        "site",
        "unique_key",
        "ip_tag",
        "user_tag",
        "start_time_tag",
        "time_tag",
        "pages_count",
        "banks_count",
        "profile_actions_count",
        "hacking",
    ]

    def user_tag(self, obj):
        if not obj.user:
            return "-"

        tag = obj.user.email
        if obj.auth == "login":
            tag += f"""<img src="{settings.STATIC_URL}site_statistics/images/icoadm_login.png" height=15 style="margin-left: 10px;" />"""

        if obj.auth == "register":
            tag += f"""<img src="{settings.STATIC_URL}site_statistics/images/icoadm_signup.png" height=15 style="margin-left: 10px;" />"""

        return mark_safe(tag)

    user_tag.short_description = "Пользователь"

    readonly_fields = fields

    list_display = fields


class SessionActionInline(BaseInline):
    model = SessionAction
    fields = ["action"]
    readonly_fields = fields

    def action(self, obj):
        return f"""{obj.time.strftime('%d.%m %H:%M:%S')}:{obj.adress}"""

    action.short_description = ""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False


class SessionModelAdmin(BaseSessionAdmin):
    inlines = [SessionActionInline]

    fields = [
        "device_tag",
        "site",
        "unique_key",
        "ip_tag",
        "start_time_tag",
        "pages_count",
        "source_count",
        "hacking",
        "hacking_reason",
        "headers",
    ]

    readonly_fields = fields

    list_display = [field for field in fields if field != "headers"]


admin.site.register(TryLoginToAdminPanel)
admin.site.register(TryLoginToFakeAdminPanel)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(SessionModel, SessionModelAdmin)
admin.site.register(SessionFilters)
