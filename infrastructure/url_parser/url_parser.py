import re

from infrastructure.url_parser.base_url_parser import UrlParserInterface


class UrlParser(UrlParserInterface):
    @staticmethod
    def remove_protocol(path: str) -> str:
        path = path.replace("https://", "")
        path = path.replace("http://", "")

        return path

    @staticmethod
    def is_source(path: str) -> bool:
        static_patterns = [
            ".png",
            "__debug__",
            ".jpg",
            ".js",
            ".css",
            ".scss",
            ".webp",
            ".WEBP",
            ".ico",
            ".jpeg",
            "styles",
            "static",
            "media",
        ]
        for static_pattern in static_patterns:
            if static_pattern in path:
                return True

        return False

    @staticmethod
    def is_ip(path: str) -> bool:
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return ip_pattern.match(path) is not None

    def get_subdomain_from_host(self, host: str) -> str:
        host = self.remove_protocol(host)
        host = host.replace("127.0.0.1", "localhost")

        if "localhost" in host:
            if "." not in host:
                return ""

            return host.split(".")[0]

        if host.count(".") < 2:
            return ""

        return host.split(".")[0]

    def get_domain_from_host(self, host: str) -> str:
        host = self.remove_protocol(host)
        host = host.replace("127.0.0.1", "localhost")

        if ":" in host:
            host = host.split(":")[0]

        subdomain = self.get_subdomain_from_host(host)
        first_domain = host.split(".")[-1]

        domain = re.findall(f"{subdomain}.*?{first_domain}", host)[0]
        domain = re.sub(subdomain, "", domain)
        if domain[0] == ".":
            domain = domain[1::]

        return domain


def get_url_parser() -> UrlParserInterface:
    return UrlParser()
