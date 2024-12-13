from dataclasses import dataclass

from domain.common.replacement_pattern import ReplacementPatternInterface
from domain.user.user import UserInterface


@dataclass
class NotificationInterface:
    message: str
    user: UserInterface


@dataclass
class NotificationPatternInterface(ReplacementPatternInterface):
    pass
