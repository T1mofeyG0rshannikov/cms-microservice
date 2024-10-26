from typing import Protocol


class IdeaRepositoryInterface(Protocol):
    def delete_idea(self, id: int) -> None:
        raise NotImplementedError()

    def get_ideas(self, category=None, sorted_by=None, status=None, user=None):
        raise NotImplementedError()

    def get_idea(self, id: int):
        raise NotImplementedError()
