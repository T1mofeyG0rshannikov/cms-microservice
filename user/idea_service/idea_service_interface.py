from typing import Any, Protocol

from user.interfaces import UserInterface


class IdeaServiceInterface(Protocol):
    def get_ideas(self, filter: str, sorted_by: str, status: str, user: UserInterface) -> dict[str, Any]:
        raise NotImplementedError()
