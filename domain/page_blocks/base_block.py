from dataclasses import dataclass


@dataclass
class TemplateInterface:
    name: str
    template: str


@dataclass
class BaseBlockInterface:
    name: str
    template: TemplateInterface
    ancor: str | None
