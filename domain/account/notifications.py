from dataclasses import dataclass

from domain.common.replacement_pattern import ReplacementPatternInterface


@dataclass
class NotificationInterface:
    message: str
    

@dataclass
class NotificationPatternInterface(ReplacementPatternInterface):
    pass