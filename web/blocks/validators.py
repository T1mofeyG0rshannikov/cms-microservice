import re


def validate_html_filename(filename: str) -> bool:
    pattern = r"^[a-zA-Z0-9_-]+\.html$"
    if re.match(pattern, filename):
        return True
    else:
        return False
