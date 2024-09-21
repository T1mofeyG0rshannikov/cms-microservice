from typing import Protocol


class IdeaRepositoryInterface(Protocol):
    @staticmethod
    def delete_idea(id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_ideas(category=None, sorted_by=None, status=None, user=None):
        raise NotImplementedError()

    @staticmethod
    def get_idea(id: int):
        raise NotImplementedError()
