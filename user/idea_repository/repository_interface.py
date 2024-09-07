from typing import Protocol

from user.models.idea import Idea


class IdeaRepositoryInterface(Protocol):
    @staticmethod
    def get_ideas(category=None, sorted_by=None, user=None) -> list[Idea]:
        raise NotImplementedError()
