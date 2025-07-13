from django.http import HttpRequest

from domain.user.repository import UserRepositoryInterface
from infrastructure.auth.jwt_processor import get_jwt_processor
from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.persistence.repositories.user_repository import get_user_repository


class JwtAuthMiddleware:
    jwt_processor: JwtProcessorInterface = get_jwt_processor()
    user_repository: UserRepositoryInterface = get_user_repository()

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        token = request.headers.get("Authorization")

        payload = self.jwt_processor.validate_token(token)

        if payload:
            user = self.user_repository.get(id=payload["id"])
        else:
            user = None

        request.user_from_header = user

        return self.get_response(request)
