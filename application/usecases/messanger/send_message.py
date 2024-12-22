from domain.messanger.repository import MessangerRepositoryInterface
from infrastructure.persistence.repositories.messanger_repositroy import (
    get_messanger_repository,
)


class SendMessage:
    def __init__(self, messanger_repository: MessangerRepositoryInterface) -> None:
        self.messanger_repository = messanger_repository

    def __call__(self, chat_id: int, user_id: int, message_text: str) -> None:
        chat_user = self.messanger_repository.get_chat_user(chat_id, user_id)

        self.messanger_repository.create_message(chat_user_id=chat_user.id, text=message_text)


def get_send_message_interactor(
    messanger_repository: MessangerRepositoryInterface = get_messanger_repository(),
) -> SendMessage:
    return SendMessage(messanger_repository=messanger_repository)
