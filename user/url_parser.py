import re


class UrlParser:
    @staticmethod
    def get_subdomain_from_host(host: str) -> str:
        host = host.replace("http://", "")
        host = host.replace("https://", "")
        host = host.replace("127.0.0.1", "localhost")

        if "localhost" in host:
            if "." not in host:
                return ""

            return host.split(".")[0]

        if host.count(".") < 2:
            return ""

        return host.split(".")[0]

    def get_domain_from_host(self, host: str) -> str:
        host = host.replace("http://", "")
        host = host.replace("https://", "")
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


def get_url_parser() -> UrlParser:
    return UrlParser()
