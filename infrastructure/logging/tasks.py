from web.core.celery import app


@app.task()
def create_raw_log(unique_key, session_data, page_adress, time, path):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    session = user_session_repository.update_or_create_raw_session(unique_key=unique_key, session_data=session_data)
    if session:
        user_session_repository.create_session_action(
            adress=page_adress, time=time, session_unique_key=unique_key, path=path
        )


@app.task()
def create_user_activity_log(
    unique_key, user_session_data, page_adress, is_disable_url_to_log, is_enable_url_to_log, time
):
    from infrastructure.persistence.repositories.user_session_repository import (
        get_user_session_repository,
    )

    user_session_repository = get_user_session_repository()
    try:
        executed_user_session = True
        user_session_repository.update_or_create_user_session(unique_key=unique_key, session_data=user_session_data)
    except:
        executed_user_session = False

    if executed_user_session:
        if not is_disable_url_to_log and is_enable_url_to_log:
            user_session_repository.create_user_action(
                adress=page_adress, session_unique_key=unique_key, text="перешёл на страницу", time=time
            )
