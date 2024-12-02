from typing import Any
from django.utils.timezone import now

from application.common.base_url_parser import UrlParserInterface
from infrastructure.url_parser import get_url_parser


def create_raw_log(
    session_id: int, page_adress: str, path: str, time=now(), url_parser: UrlParserInterface = get_url_parser()
) -> dict[str, Any]:
    is_page = None
    is_source = None

    is_page = False if url_parser.is_source(path) else True
    is_source = not is_page

    return {
        "adress": page_adress,
        "time": time,
        "is_page": is_page,
        "is_source": is_source,
        "session_id": session_id,
    }
    

def create_user_log(session_id: int, adress: str, text: str, time=now()) -> dict[str, Any]:
    return {"adress": adress, "time": time, "session_id": session_id, "text": text}