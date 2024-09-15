from typing import Protocol

from user.models.idea import Idea


class IdeaRepositoryInterface(Protocol):
    @staticmethod
    def delete_idea(id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_ideas(category=None, sorted_by=None, status=None, user=None) -> list[Idea]:
        raise NotImplementedError()

    @staticmethod
    def get_idea(id: int) -> Idea:
        raise NotImplementedError()
