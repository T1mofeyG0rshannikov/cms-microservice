from infrastructure.persistence.models.site_statistics import PenaltyLog


class AddPenaltyLog:
    def __call__(self, session_id: int, text: str) -> None:
        PenaltyLog.objects.create(
            session_id=session_id,
            text=text,
        )