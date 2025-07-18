from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db import models
from django.utils.safestring import mark_safe

from infrastructure.admin.admin_settings import get_admin_settings


class MyAdminSite(AdminSite):
    site_header = "Bankomag"
    index_title = "bankomag"

    def get_app_list(self, request, app_label=None):
        app_order = [
            "user",
            "site_statistics",
            "system",
            "catalog",
            "materials",
            "blocks",
            "settings",
            "notifications",
            "account",
            "common",
            "styles",
            "site_tests",
        ]
        app_order_dict = dict(zip(app_order, range(len(app_order))))
        app_list = list(self._build_app_dict(request).values())
        app_list.sort(key=lambda x: app_order_dict.get(x["app_label"], 0))

        return app_list


admin.site = MyAdminSite()


def redirect_to_change_page_tag(model_instance: models.Model, value: str) -> str:
    settings = get_admin_settings()
    return mark_safe(
        f"""<a href="/{settings.admin_url}/{model_instance._meta.app_label}/{model_instance._meta.model_name}/{model_instance.pk}/change/">{value}</a>"""
    )
