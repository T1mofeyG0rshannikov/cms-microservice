from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.models import User


class JwtAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()

    def __call__(self, request):
        token = request.headers.get("Authorization")
        payload = self.jwt_processor.validate_token(token)

        if payload:
            user = User.objects.get_user_by_id(payload["id"])
        else:
            user = None

        request.user_from_header = user

        return self.get_response(request)
