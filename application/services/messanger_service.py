from domain.messanger.repository import MessangerRepositoryInterface
from domain.referrals.referral import ReferralInterface
from domain.referrals.repository import ReferralRepositoryInterface
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

    def get_chats(self, user: ReferralInterface):
        # referral = self.referral_repository.get(sponsors_id=user.id)
        referral = user.sponsor

        chats = self.messanger_repository.get_chats(user.id)
        chat_dicts = []

        if referral:
            print(chats, 0)
            referral_chat_user = self.messanger_repository.get_referral_chat(user.id, referral.id)
            chatuserss = [
                referral_chat_user,
                *[chatuser for chatuser in self.messanger_repository.get_last_chatted_with(user)],
            ]
            chats, last_messages = self.messanger_repository.get_messages(user.id)

            print(chatuserss)
            print(last_messages)

            for i in range(len(chats)):
                chat_dicts.append({"chat_user": chatuserss[i], "message": last_messages[i]})
            print(chat_dicts, 1)
            return chat_dicts

        chatuserss = [
            *[chatuser for chatuser in self.messanger_repository.get_last_chatted_with(user)],
        ]

        chats, last_messages = self.messanger_repository.get_messages(user.id)

        for i in range(len(chats)):
            chat_dicts.append(
                {
                    "chat_user": chatuserss[i],
                    "message": last_messages[i],
                }
            )

        print(chat_dicts, 2)
        return chat_dicts

    def get_chat(self, user_id: int, chat_id: int):
        messages = self.messanger_repository.get_chat_messages(user_id=user_id, chat_id=chat_id)
        interlocutor = self.messanger_repository.get_interlocuter(user_id, chat_id=chat_id)

        return {"messages": messages, "interlocutor": interlocutor}


def get_messanger_service(
    referral_repository: ReferralRepositoryInterface = get_referral_repository(),
    messanger_repository: MessangerRepositoryInterface = get_messanger_repository(),
):
    return MessangerService(referral_repository=referral_repository, messanger_repository=messanger_repository)
