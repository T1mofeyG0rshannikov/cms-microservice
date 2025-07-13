from typing import Protocol


class JwtProcessorInterface(Protocol):
    def create_token(self, data: dict, hours: int = None) -> str:
        raise NotImplementedError

    def validate_token(self, token: str) -> dict | None:
        raise NotImplementedError
