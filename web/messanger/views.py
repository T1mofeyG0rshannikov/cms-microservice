import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from application.services.messanger_service import get_messanger_service
from application.usecases.messanger.send_message import get_send_message_interactor
from infrastructure.requests.request_interface import RequestInterface
from web.user.views.base_user_view import APIUserRequired


class GetChatsView(APIUserRequired):
    messanger_service = get_messanger_service()

    def get(self, request: RequestInterface) -> JsonResponse:
        user = request.user

        chats = self.messanger_service.get_chats(user)
        print(chats)
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name="dispatch")
class SendMessageView(APIUserRequired):
    send_message_interactor = get_send_message_interactor()

    def post(self, request: RequestInterface) -> HttpResponse:
        user = request.user
        data = json.loads(request.body)

        chat_id = data.get("chat_id")
        message_text = data.get("message_text")
        print(chat_id)

        self.send_message_interactor(chat_id=chat_id, user_id=user.id, message_text=message_text)

        return HttpResponse(status=201)
