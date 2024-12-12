from collections.abc import Iterable
from typing import Any, Protocol

from domain.common.screen import ScreenInterface
from domain.user.idea import IdeaInterface


class IdeaRepositoryInterface(Protocol):
    def delete(self, id: int) -> None:
        raise NotImplementedError

    def create_like(self, user_id: int, idea_id: int) -> None:
        raise NotImplementedError

    def get_ideas(self, category=None, sorted_by=None, status=None, user_id: int = None) -> Iterable[IdeaInterface]:
        raise NotImplementedError

    def get(self, id: int) -> IdeaInterface:
        raise NotImplementedError

    def update(self, idea_id: int, **kwargs) -> None:
        raise NotImplementedError

    def get_screens(self, idea_id: int):
        raise NotImplementedError

    def get_screen_names(self, idea_id: int) -> list[str]:
        raise NotImplementedError

    def create_screen(self, fields: dict[str, Any]) -> None:
        raise NotImplementedError

    def delete_like(self, user_id: int, idea_id: int) -> None:
        raise NotImplementedError

    def like_exists(self, user_id: int, idea_id: int) -> bool:
        raise NotImplementedError

    def create(self, screens: Iterable[ScreenInterface], **kwargs) -> None:
        raise NotImplementedError

    def delete_screens(self, idea_id: int, old_screens: list[str]) -> None:
        raise NotImplementedError
