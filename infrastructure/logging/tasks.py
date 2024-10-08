from web.core.celery import app


@app.task()
def create_raw_logs(logs):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()

    user_session_repository.bulk_create_raw_session_logs(logs)


@app.task()
def create_user_activity_logs(logs):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()

    user_session_repository.bulk_create_user_session_logs(logs)
