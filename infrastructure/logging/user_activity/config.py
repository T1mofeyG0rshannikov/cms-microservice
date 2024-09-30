from functools import lru_cache

from django.conf import settings

from infrastructure.admin.admin_settings import get_admin_settings


class UserActivitySettings:
    enable_adresses = [get_admin_settings().admin_url]
    disable_user_session_urls_to_logg = [get_admin_settings().admin_url + "/jsi18n/"]
    exclude_urls = [
        settings.STATIC_URL,
        settings.MEDIA_URL,
        "/styles/",
        # get_admin_settings().admin_url,
        "set-token",
        "site_statistics/opened-product-popup",
        "site_statistics/opened-product-link",
        "site_statistics/opened-product-promo",
        "site_statistics/opened-change-password-form",
        "site_statistics/opened-update-user-form",
        "site_statistics/increment-banks-count",
        "register",
        "login",
        "get-change-user-form",
        "change-user",
        "change-site",
        "get-change-site-form",
        "get-create-user-product-form",
        "get-choice-product-form",
        "get-product-description-popup",
        "add-user-product",
        "delete-user-product",
        "/user/get-user-info",
        "get-template-",
        "/null",
    ]


@lru_cache
def get_user_active_settings() -> UserActivitySettings:
    return UserActivitySettings()
