from domain.user.exceptions import CantAddLike, IdeaNotFound, LikeAlreadyExists
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class AddLike:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, idea_id: int, user_id: int) -> None:
        idea = self.repository.get(idea_id)

        if not idea:
            raise IdeaNotFound(f'No idea with id "{idea_id}"')

        if idea.user_id == user_id:
            raise CantAddLike("You cant like your own ideas")

        like_exists = self.repository.like_exists(user_id, idea.id)

        if like_exists:
            raise LikeAlreadyExists("You already had liked this idea")

        self.repository.create_like(user_id, idea.id)


def get_add_like_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> AddLike:
    return AddLike(idea_repository)
