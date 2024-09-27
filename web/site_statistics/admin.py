from django.conf import settings
from django.contrib import admin
from django.utils.html import mark_safe

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


class UserActivityAdmin(admin.ModelAdmin):
    inlines = [UserActionInline]

    fields = [
        "device_tag",
        "site",
        "unique_key",
        "ip",
        "start_time_tag",
        "banks_count",
        "profile_actions_count",
        "pages_count",
        "user_tag",
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

    def start_time_tag(self, obj):
        return obj.start_time.strftime("%d.%m %H:%M:%S")

    start_time_tag.short_description = "Дата"

    def device_tag(self, obj):
        if obj.device:
            src = f"{settings.STATIC_URL}site_statistics/images/icoadm_desktop.png"
        else:
            src = f"{settings.STATIC_URL}site_statistics/images/icoadm_smart.png"

        return mark_safe(f"""<img height="30" src={src} />""")

    device_tag.short_description = "Устройство"
    readonly_fields = [
        "device_tag",
        "site",
        "unique_key",
        "ip",
        "start_time_tag",
        "banks_count",
        "profile_actions_count",
        "pages_count",
        "user_tag",
    ]

    list_display = fields

    class Media:
        css = {"all": ("site_statistics/css/user_action_admin.css",)}


class SessionActionInline(BaseInline):
    model = SessionAction
    fields = ["action"]
    readonly_fields = fields

    def action(self, obj):
        return f"""{obj.time.strftime('%d.%m %H:%M:%S')}:{r"     "}{obj.adress}"""

    action.short_description = ""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False


class SessionModelAdmin(admin.ModelAdmin):
    inlines = [SessionActionInline]

    fields = [
        "device_tag",
        "site",
        "unique_key",
        "ip",
        "start_time_tag",
        "pages_count",
        "hacking",
        "hacking_reason",
    ]

    def start_time_tag(self, obj):
        return obj.start_time.strftime("%d.%m %H:%M:%S")

    start_time_tag.short_description = "Дата"

    def device_tag(self, obj):
        if obj.device:
            src = f"{settings.STATIC_URL}site_statistics/images/icoadm_desktop.png"
        else:
            src = f"{settings.STATIC_URL}site_statistics/images/icoadm_smart.png"

        return mark_safe(f"""<img height="30" src={src} />""")

    device_tag.short_description = "Устройство"
    readonly_fields = fields

    list_display = fields

    class Media:
        css = {"all": ("site_statistics/css/user_action_admin.css",)}


admin.site.register(TryLoginToAdminPanel)
admin.site.register(TryLoginToFakeAdminPanel)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(SessionModel, SessionModelAdmin)
admin.site.register(SessionFilters)
