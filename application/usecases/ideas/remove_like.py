from domain.user.exceptions import IdeaNotFound
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class RemoveLike:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, idea_id: int, user_id: int) -> None:
        idea = self.repository.get_idea(idea_id)

        if not idea:
            raise IdeaNotFound(f'no idea with id "{idea_id}"')

        self.repository.delete_like(user_id, idea_id)


def get_remove_like_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> RemoveLike:
    return RemoveLike(idea_repository)
