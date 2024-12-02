from typing import Protocol


class ErrorLogRepositoryInterface(Protocol):
    def create_error_log(self, **kwargs) -> None:
        raise NotImplementedError
