from collections.abc import Iterable

from domain.common.screen import ScreenInterface


def valid_screens_size(screens: Iterable[ScreenInterface], max_size: int, error_message: str) -> dict[str, list[str]]:
    errors = {}
    for i, screen in enumerate(screens):
        if screen.size > max_size:
            errors[f"file{i + 1}"] = [error_message]

    return errors
