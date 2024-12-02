from dataclasses import dataclass


@dataclass
class ReplacementPatternInterface:
    method: str
    arg: str
    tag: str
    text: str