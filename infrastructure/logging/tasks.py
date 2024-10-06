from django.utils.timezone import now

from application.services.domains.url_parser import get_url_parser
from application.sessions.dto import RawSessionDTO
from web.core.celery import app


@app.task()
def create_raw_log(unique_key, page_adress, path, time=now()):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    url_parser = get_url_parser()

    if "null" not in path:
        increment_field = "source_count" if url_parser.is_source(path) else "pages_count"

        user_session_repository.increment_raw_session_field(unique_key, increment_field)

    user_session_repository.create_session_action(page_adress, unique_key, time)


@app.task()
def create_raw_session(session_data: dict):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    user_session_repository.create_raw_session(session_data)


@app.task()
def update_raw_session_unique_key(cookie_unique_key, unique_key):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    user_session_repository.update_raw_session_unique_key(cookie_unique_key, unique_key)


@app.task()
def update_raw_session(unique_key, end_time, hacking, hacking_reason):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    user_session_repository.update_raw_session(
        unique_key,
        end_time=end_time,
        hacking=hacking,
        hacking_reason=hacking_reason,
    )


@app.task()
def create_user_activity_log(unique_key, page_adress, time):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()

    user_session_repository.increment_user_session_field(unique_key, "pages_count")

    user_session_repository.create_user_action(
        adress=page_adress, session_unique_key=unique_key, text="перешёл на страницу", time=time
    )


@app.task()
def create_raw_logs(logs):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()

    user_session_repository.bulk_create_raw_session_logs(logs)
