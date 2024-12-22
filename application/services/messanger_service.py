from domain.messanger.repository import MessangerRepositoryInterface
from domain.referrals.repository import ReferralRepositoryInterface
from domain.user.user import UserInterface
from infrastructure.persistence.repositories.messanger_repositroy import (
    get_messanger_repository,
)
from infrastructure.persistence.repositories.referral_repository import (
    get_referral_repository,
)


class MessangerService:
    def __init__(
        self, referral_repository: ReferralRepositoryInterface, messanger_repository: MessangerRepositoryInterface
    ) -> None:
        self.referral_repository = referral_repository
        self.messanger_repository = messanger_repository

    def get_chats(self, user: UserInterface):
        referral = self.referral_repository.get(sponsors_id=user.id)
        chats = self.messanger_repository.get_chats(user.id)
        referral_chat_user = self.messanger_repository.get_referral_chat(user.id, referral.id)
        chatuserss = [
            referral_chat_user,
            *[chatuser for chatuser in self.messanger_repository.get_last_chatted_with(user, chats)],
        ]
        chats, last_messages = self.messanger_repository.get_messages(chats, user.id)

        chats = []
        for i in range(len(last_messages)):
            chats.append({"chat_user": chatuserss[i], "message": last_messages[i]})

        return chats

    def get_chat(self, user_id: int, chat_id: int):
        messages = self.messanger_repository.get_chat_messages(user_id=user_id, chat_id=chat_id)
        interlocutor = self.messanger_repository.get_interlocuter(user_id, chat_id=chat_id)

        return {"messages": messages, "interlocutor": interlocutor}


def get_messanger_service(
    referral_repository: ReferralRepositoryInterface = get_referral_repository(),
    messanger_repository: MessangerRepositoryInterface = get_messanger_repository(),
):
    return MessangerService(referral_repository=referral_repository, messanger_repository=messanger_repository)
