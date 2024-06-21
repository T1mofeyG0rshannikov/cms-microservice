from django.contrib.auth import authenticate

from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.models import User
from user.user_manager.user_manager_interface import UserManagerInterface


class JwtAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()

    def __call__(self, request):
        """token = request.headers.get("Authorization")
        payload = self.jwt_processor.validate_token(token)
        print(token, payload)
        if payload:
            user = self.user_manager.get_user_by_id(payload["id"])
        else:
            user = request.user

        print(user, "1")
        #print(request.user)
        request.user = user
        authenticate(request)"""

        return self.get_response(request)
