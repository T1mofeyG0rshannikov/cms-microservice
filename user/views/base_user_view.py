from django.views.generic import TemplateView

from user.auth.jwt_processor import get_jwt_processor
from user.auth.jwt_processor_interface import JwtProcessorInterface


class BaseUserView(TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.jwt_processor: JwtProcessorInterface = get_jwt_processor()
