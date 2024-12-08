from collections.abc import Iterable

from domain.user.idea import IdeaInterface
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class GetIdeas:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, filter: str, sorted_by: str, status: str, user_id: int) -> Iterable[IdeaInterface]:
        idea_user = None
        category = None

        if filter == "my":
            idea_user = user_id

        elif filter:
            category = filter

        return self.repository.get_ideas(category=category, user_id=idea_user, status=status, sorted_by=sorted_by)


def get_get_ideas_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> GetIdeas:
    return GetIdeas(idea_repository)
