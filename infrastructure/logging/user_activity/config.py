from functools import lru_cache

from django.conf import settings

from infrastructure.admin.admin_settings import get_admin_settings


class UserActivitySettings:
    enable_adresses = [get_admin_settings().admin_url]
    exclude_urls = [
        settings.STATIC_URL,
        settings.MEDIA_URL,
        "/styles/",
        get_admin_settings().admin_url,
        "set-token",
        "site_statistics",
        "register",
        "login",
        "get-change-user-form",
        "change-user",
        "change-site",
        "get-template-products",
        "get-template-site",
        "get-change-site-form",
        "get-create-user-product-form",
        "get-choice-product-form",
        "get-product-description-popup",
        "add-user-product",
        "delete-user-product",
        "/user/get-user-info",
    ]


@lru_cache
def get_user_active_settings() -> UserActivitySettings:
    return UserActivitySettings()
