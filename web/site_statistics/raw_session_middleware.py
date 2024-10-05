import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from application.common.url_parser import UrlParserInterface
from application.services.domains.url_parser import get_url_parser
from domain.user_sessions.repository import UserSessionRepositoryInterface
from infrastructure.persistence.models.site_statistics import SessionAction, SessionModel
from infrastructure.persistence.repositories.user_session_repository import (
    get_user_session_repository,
)
from infrastructure.persistence.sessions.service import RawSessionService
from infrastructure.requests.service import get_request_service

#logger = logging.getLogger("main")

def update_raw_session_unique_key(cookie_unique_key, unique_key):
    user_session_repository = get_user_session_repository()
    user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)


def update_raw_session(unique_key, end_time, hacking, hacking_reason):
    user_session_repository = get_user_session_repository()
    user_session_repository.update_raw_session(
        unique_key,
        end_time=end_time,
        hacking=hacking,
        hacking_reason=hacking_reason,
    )


def create_raw_log(unique_key, page_adress, path, time=now()) -> SessionAction:
    url_parser = get_url_parser()

    if "null" not in path:
        is_page = False if url_parser.is_source(path) else True
        is_source = not is_page

    return SessionAction(
        adress=page_adress,
        time=time,
        is_page=is_page,
        is_source=is_source,
        session_id=SessionModel.objects.values_list("id", flat=True).get(unique_key=unique_key),
    )



def create_raw_session(session_data: dict):
    user_session_repository = get_user_session_repository()
    user_session_repository.create_raw_session(**session_data)


class RawSessionMiddleware:
    url_parser: UrlParserInterface = get_url_parser()
    user_session_repository: UserSessionRepositoryInterface = get_user_session_repository()
    session_key = settings.RAW_SESSION_SESSION_KEY
    logs_array_length = 10
    logs = []

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        raw_session_service = RawSessionService(get_request_service(request), self.user_session_repository, self.url_parser)
        path = request.get_full_path()
        site = request.get_host()
        page_adress = site + path
        host = site.split(":")[0]
        port = site.split(":")[1] if ":" in site else None
        #logger.info("start 0")
        unique_key = request.session.session_key
        #logger.info("first unique_key 0")
        if not unique_key:
            request.session.save()
        #logger.info("saved session")
        unique_key = request.session.session_key

        cookie = request.COOKIES.get(settings.USER_ACTIVITY_COOKIE_NAME)
        #logger.info("get cookie")
        response = self.get_response(request)
        #logger.info("get response")

        if path == "/user/get-user-info":
            return response
        # cookie = None
        if not cookie:
            expires = datetime.utcnow() + timedelta(days=365 * 10)
            response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

            session_data = raw_session_service.get_initial_raw_session(
                unique_key, path, site, request.user_agent.is_mobile
            )
            # print(1, session_data)
            #logger.info("create new cookie session 1")
            create_raw_session(session_data.__dict__)
            #self.user_session_repository.create_raw_session(**session_data.__dict__)
            #logger.info("create raw log 2")
            self.logs.append(create_raw_log(unique_key, page_adress, path, time=now()))
        else:
            cookie_unique_key = cookie
            if cookie_unique_key == unique_key:
                session_data = raw_session_service.get_initial_raw_session(
                    unique_key, path, site, request.user_agent.is_mobile
                )
                session_data = raw_session_service.filter_sessions(session_data, host, page_adress, port)

                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    #logger.info("create raw session 3")
                    create_raw_session(session_data.__dict__)
                    #self.user_session_repository.create_raw_session(**session_data.__dict__)
                else:
                    #logger.info("update raw session 4")
                    update_raw_session(unique_key, now(), session_data.hacking, session_data.hacking_reason)
                    '''self.user_session_repository.update_raw_session(
                        unique_key,
                        end_time=now(),
                        hacking=session_data.hacking,
                        hacking_reason=session_data.hacking_reason,
                    )'''

                # print(2, session_data)
            else:
                expires = datetime.utcnow() + timedelta(days=365 * 10)
                response.set_cookie(settings.USER_ACTIVITY_COOKIE_NAME, f"{unique_key}", expires=expires)

                if not self.user_session_repository.is_raw_session_exists(cookie_unique_key):
                    session_data = raw_session_service.get_initial_raw_session(
                        cookie_unique_key, path, site, request.user_agent.is_mobile
                    )
                    #logger.info("сreate raw session 5")
                    create_raw_session(session_data.__dict__)
                    #self.user_session_repository.create_raw_session(**session_data.__dict__)
                    if not self.user_session_repository.is_raw_session_exists(unique_key):
                        #logger.info("update raw session 6")
                        update_raw_session_unique_key(cookie_unique_key, unique_key)
                        #self.user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)

                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    #logger.info("update raw session 7")
                    update_raw_session_unique_key(cookie_unique_key, unique_key)
                    #self.user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)

                #logger.info("get raw session 8")
                session_data = self.user_session_repository.get_raw_session(unique_key)
                session_data = raw_session_service.get_initial_raw_session(
                    unique_key, path, site, request.user_agent.is_mobile
                )
                if not self.user_session_repository.is_raw_session_exists(unique_key):
                    #logger.info("create raw session 9")
                    create_raw_session(session_data.__dict__)
                    #self.user_session_repository.create_raw_session(**session_data.__dict__)
                #logger.info("create raw log 10")
                self.logs.append(create_raw_log(unique_key, page_adress, path, time=now()))
                # print(3, session_data)

        if session_data.hacking:
            return HttpResponse(status=503)

        #logger.info("create raw log 11")
        self.logs.append(create_raw_log(unique_key, page_adress, path, time=now()))
        
        if len(self.logs) > self.logs_array_length:
            print(self.logs, "LLLLOGGGS")
            SessionAction.objects.bulk_create(self.logs)
            self.logs.clear()

        return response
