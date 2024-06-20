from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.user_manager.user_manager import get_user_manager
from user.user_manager.user_manager_interface import UserManagerInterface


class JwtAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_manager: UserManagerInterface = get_user_manager()
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()

    def __call__(self, request):
        token = request.headers.get("Authorization")
        payload = self.jwt_processor.validate_token(token)

        if payload:
            user = self.user_manager.get_user_by_id(payload["id"])
        else:
            user = None

        request.user = user

        return self.get_response(request)
