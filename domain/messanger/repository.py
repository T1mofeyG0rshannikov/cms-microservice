from collections.abc import Iterable
from typing import Protocol

from domain.messanger.entities import ChatUserInterface
from domain.referrals.referral import ReferralInterface
from domain.user.entities import UserInterface


class MessangerRepositoryInterface(Protocol):
    def get_chat_user(self, chat_id: int, user_id: int) -> ChatUserInterface:
        raise NotImplementedError

    def create_message(self, chat_user_id: int, text: str):
        raise NotImplementedError

    def get_chat_messages(self, user_id: int, chat_id: int):
        raise NotImplementedError

    def get_interlocuter(self, user_id: int, chat_id: int) -> UserInterface:
        raise NotImplementedError

    def get_referral_chat(self, user_id: int, referral_id: int):
        raise NotImplementedError

    def get_messages(self, user_id: int):
        raise NotImplementedError

    def get_last_chatted_with(self, user: ReferralInterface) -> Iterable[ChatUserInterface]:
        raise NotImplementedError

    def get_chats(self, user_id: int):
        raise NotImplementedError
