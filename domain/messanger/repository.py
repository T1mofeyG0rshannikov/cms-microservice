from typing import Protocol

from domain.messanger.entities import ChatUserInterface


class MessangerRepositoryInterface(Protocol):
    def get_chat_user(self, chat_id: int, user_id: int) -> ChatUserInterface:
        raise NotImplementedError

    def create_message(self, chat_user_id: int, text: str):
        raise NotImplementedError
