from dataclasses import dataclass
from datetime import datetime

from django.conf import settings
from django.http import HttpRequest
from django.utils.timezone import now

from infrastructure.get_ip import get_client_ip
from infrastructure.logging.user_activity.config import get_user_active_settings
from web.site_statistics.models import UserAction, UserActivity


@dataclass
class UserActivityDTO:
    unique_key: str
    ip: str
    start_time: datetime
    end_time: datetime
    site: str
    banks_count: int = 0
    pages_count: int = 0
    popups_count: int = 0
    auth: str = None


class UserActivityMiddleware:
    session_key = "user_activity"
    settings = get_user_active_settings()

    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_urls = self.settings.exclude_urls
        self.enabled_adresses = self.settings.enable_adresses

    def is_enable_url_to_log(self, path: str) -> bool:
        for url in self.exclude_urls:
            if url in path:
                return False

        return True

    def __call__(self, request: HttpRequest):
        # del request.session[self.session_key]
        # request.session.save()

        path = request.build_absolute_uri()

        for enable_adress in self.enabled_adresses:
            if enable_adress in path:
                return self.get_response(request)

        site = request.get_host()

        user = str(request.user)

        ip = get_client_ip(request)
        unique_key = f"{site}-{ip}"

        session_data = UserActivityDTO(
            ip=ip, start_time=now().isoformat(), unique_key=unique_key, end_time=now().isoformat(), site=site
        ).__dict__

        print(session_data)

        if self.session_key not in request.session:
            request.session[self.session_key] = session_data

            request.session.save()

            session_data = request.session[self.session_key]
            print(session_data)

            session_db, _ = UserActivity.objects.get_or_create(
                unique_key=request.session[self.session_key]["unique_key"], defaults=session_data
            )

            UserAction.objects.create(adress=page_adress, session=session_db, text="перешёл на страницу")
            request.session[self.session_key]["pages_count"] += 1

            UserActivity.objects.update_or_create(unique_key=session_data["unique_key"], defaults=session_data)

            return self.get_response(request)

        response = self.get_response(request)
        if not self.is_enable_url_to_log(path) or response.status_code != 200:
            return response

        if "popup" in path:
            request.session[self.session_key]["popups_count"] += 1

        page_adress = request.get_host() + request.get_full_path()

        print(request.session[self.session_key], "SESSION")
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
