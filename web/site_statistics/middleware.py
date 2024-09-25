from dataclasses import dataclass
from datetime import datetime

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from infrastructure.admin.admin_settings import get_admin_settings
from infrastructure.get_ip import get_client_ip
from web.site_statistics.models import UserAction, UserActivity


@dataclass
class UserActivityDTO:
    unique_key: str
    ip: str
    start_time: datetime
    end_time: datetime
    banks_count: int = 0
    pages_count: int = 0
    popups_count: int = 0
    auth: str = None


class UserActivityMiddleware:
    session_key = "user_activity"
    admin_settings = get_admin_settings()

    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = [
            settings.STATIC_URL,
            settings.MEDIA_URL,
            "/styles/",
            self.admin_settings.admin_url,
            "set-token",
            "site_statistics",
            "register",
            "login",
            "get-change-user-form",
            "change-user",
            "get-change-site-form",
            "get-create-user-product-form",
            "get-choice-product-form",
            "get-product-description-popup",
            "add-user-product",
            "delete-user-product",
        ]

    def is_enable_url_to_log(self, path: str) -> bool:
        for url in self.exclude_urls:
            if url in path:
                return False

        return True

    def __call__(self, request: HttpRequest):
        path = request.build_absolute_uri()

        user = str(request.user)

        ip = get_client_ip(request)
        unique_key = f"{now().isoformat()}-{ip}-{user}"

        session_data = UserActivityDTO(
            ip=ip, start_time=now().isoformat(), unique_key=unique_key, end_time=now().isoformat()
        ).__dict__

        print(session_data)

        if self.session_key not in request.session:
            request.session[self.session_key] = session_data

            request.session.save()

            session_data = request.session[self.session_key]
            print(session_data)

            UserActivity.objects.update_or_create(unique_key=session_data["unique_key"], defaults=session_data)

            return self.get_response(request)

        response = self.get_response(request)
        if not self.is_enable_url_to_log(path) or response.status_code != 200:
            return response

        print(path)
        if "popup" in path:
            request.session[self.session_key]["popups_count"] += 1

        page_adress = request.get_host() + request.get_full_path()

        print(request.session[self.session_key])

        session_db, _ = UserActivity.objects.get_or_create(
            unique_key=request.session[self.session_key]["unique_key"], defaults=session_data
        )

        UserAction.objects.create(adress=page_adress, session=session_db, text="перешёл на страницу")
        request.session[self.session_key]["pages_count"] += 1

        if request.user.is_authenticated:
            request.session[self.session_key]["auth"] = "login"
            session_data = request.session[self.session_key]

            session_data["unique_key"] = request.session[self.session_key]["unique_key"].replace("AnonymousUser", user)
            print(session_data)
            UserActivity.objects.update_or_create(unique_key=session_data["unique_key"], defaults=session_data)

            request.session[self.session_key]["unique_key"] = request.session[self.session_key]["unique_key"].replace(
                "AnonymousUser", user
            )

        request.session[self.session_key]["end_time"] = now().isoformat()

        request.session.save()

        session_data = request.session[self.session_key]
        print(session_data)

        UserActivity.objects.update_or_create(unique_key=session_data["unique_key"], defaults=session_data)

        return response
