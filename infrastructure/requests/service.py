from django.http import HttpRequest


class RequestService:
    def __init__(self, request: HttpRequest):
        self.request = request

    def get_all_headers_to_string(self) -> str:
        str_headers = ""
        for key, value in self.request.META.items():
            if "HTTP" in key:
                str_headers += f"""{key}: {value}\n"""

        return str_headers
