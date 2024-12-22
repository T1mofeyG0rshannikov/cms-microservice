from django.http import HttpRequest

from application.services.messanger_service import get_messanger_service
from web.messanger.serializers import InterlocutorSerializer, MesageSerializer


def get_chat_body_context(request: HttpRequest, messanger_service=get_messanger_service()):
    user = request.user
    chat_id = int(request.GET.get("chat_id"))
    chat_data = messanger_service.get_chat(user_id=user.id, chat_id=chat_id)

    messages = MesageSerializer(chat_data["messages"], many=True).data
    interlocutor = InterlocutorSerializer(chat_data["interlocutor"]).data

    return {"messages": messages, "interlocutor": interlocutor}
