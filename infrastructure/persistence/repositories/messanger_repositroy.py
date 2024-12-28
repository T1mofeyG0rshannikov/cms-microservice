from collections.abc import Iterable

from django.db.models import OuterRef, Q, QuerySet, Subquery

from domain.messanger.entities import ChatUserInterface
from domain.messanger.repository import MessangerRepositoryInterface
from domain.referrals.referral import ReferralInterface
from infrastructure.persistence.models.messanger import Chat, ChatUser, Message
from infrastructure.persistence.models.user.user import User


class MessangerRepository(MessangerRepositoryInterface):
    def __get_chats_query(self, user_id: int) -> QuerySet[Chat]:
        return Chat.objects.filter(chat_users__user_id=user_id)

    def get_chat_user(self, chat_id: int, user_id: int) -> ChatUserInterface:
        return ChatUser.objects.get(chat_id=chat_id, user_id=user_id)

    def get_chat_messages(self, user_id: int, chat_id: int):
        chat = Chat.objects.get(chat_users__user_id=user_id, id=chat_id)
        return Message.objects.filter(chat_user__chat=chat)

    def get_chats(self, user_id: int):
        return self.__get_chats_query(user_id)

    def get_last_chatted_with(self, user: ReferralInterface) -> Iterable[ChatUserInterface]:
        chats = self.__get_chats_query(user.id)

        return (
            ChatUser.objects.filter(chat__in=chats)
            .exclude(Q(user_id=user.id) | Q(user_id=user.sponsor.id))
            .order_by("messages__time")
        )

    def create_message(self, chat_user_id: int, text: str):
        return Message.objects.create(chat_user_id=chat_user_id, text=text)

    def create_chat(self, user_id, interlocuter_id) -> tuple[ChatUser, ChatUser]:
        chat = Chat.objects.create()
        chat_user = ChatUser.objects.create(user_id=user_id, chat_id=chat.id)
        chat_interlocuter = ChatUser.objects.create(user_id=interlocuter_id, chat_id=chat.id)
        return chat_user, chat_interlocuter

    def count_unreadable(self, user_id) -> int:
        return (
            Message.objects.filter(chat_user__chat__chat_users__user_id=user_id, readen=False)
            .exclude(chat_user__user_id=user_id)
            .count()
        )

    def get_referral_chat(self, user_id: int, referral_id):
        chat = (
            Chat.objects.filter(Q(chat_users__user_id=user_id) | Q(chat_users__user_id=referral_id)).distinct().first()
        )
        if chat:
            return ChatUser.objects.get(chat_id=chat.id, user_id=referral_id)

        chat_user, chat_referral = self.create_chat(user_id, referral_id)

        return chat_referral

    def get_interlocuter(self, user_id: int, chat_id: int):
        interlocuter_id = ChatUser.objects.exclude(user_id=user_id).get(chat_id=chat_id).user_id
        return User.objects.values("username", "profile_picture", "last_login", "second_name", "id").get(
            id=interlocuter_id
        )

    def get_messages(self, user_id: int):
        messages_qs = Message.objects.filter(chat_user__chat__id=OuterRef("chat_users__chat__id")).order_by("-time")

        users_qs = ChatUser.objects.filter(chat=OuterRef("id")).exclude(user_id=user_id)

        chats = (
            self.__get_chats_query(user_id)
            .annotate(
                last_message=Subquery(messages_qs.values("id")[:1]), interlocutor=Subquery(users_qs.values("id")[:1])
            )
            .distinct()
        )

        id_list = [x.last_message for x in chats if x.last_message is not None]

        objects = Message.objects.in_bulk(id_list)

        result = [objects.get(id.last_message) if id.last_message is not None else None for id in chats]

        return chats, result


def get_messanger_repository() -> MessangerRepositoryInterface:
    return MessangerRepository()
