from domain.user_sessions.repository import UserSessionRepositoryInterface


class IncrementSessionCount:
    def __init__(self, repository: UserSessionRepositoryInterface, field_name: str) -> None:
        self.user_session_repository = repository
        self.session_field_name = field_name

    def __call__(self, session_id: int, adress: str, text: str) -> None:
        self.user_session_repository.increment_user_session_field(session_id, self.session_field_name)

        self.user_session_repository.create_user_action(
            adress=adress,
            text=text,
            session_id=session_id,
        )
