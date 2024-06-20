from django.views.generic import TemplateView

from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface
from user.user_manager.user_service import get_user_manager
from user.user_manager.user_manager_interface import UserManagerInterface


class BaseUserView(TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()
        self.user_manager: UserManagerInterface = get_user_manager()
