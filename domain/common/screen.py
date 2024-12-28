from dataclasses import dataclass


@dataclass
class FileInterface:
    size: int
    name: str


@dataclass
class ScreenInterface(FileInterface):
    pass


@dataclass
class ImageInterface(FileInterface):
    url: str
