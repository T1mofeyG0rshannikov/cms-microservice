from typing import Protocol


class RequestServiceInterface(Protocol):
    def get_all_headers_to_string(self) -> str:
        raise NotImplementedError

    def get_client_ip(self) -> str:
        raise NotImplementedError

    def get_all_headers(self) -> dict:
        raise NotImplementedError
