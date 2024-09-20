from typing import Protocol


class ErrorLogRepositoryInterface(Protocol):
    @staticmethod
    def create_error_log(**kwargs) -> None:
        raise NotImplementedError()
