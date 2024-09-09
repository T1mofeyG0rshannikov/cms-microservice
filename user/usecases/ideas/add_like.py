from user.exceptions import CantAddLike, IdeaNotFound, LikeAlreadyExists
from user.idea_repository.repository_interface import IdeaRepositoryInterface
from user.interfaces import UserInterface


class AddLike:
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def __call__(self, idea_id: int, user: UserInterface) -> None:
        idea = self.repository.get_idea(idea_id)

        if not idea:
            raise IdeaNotFound(f'No idea with id "{idea_id}"')

        if idea.user == user:
            raise CantAddLike("You cant like your own ideas")

        like_exists = self.repository.like_exists(user.id, idea.id)

        if like_exists:
            raise LikeAlreadyExists("You already had liked this idea")

        self.repository.create_like(user.id, idea.id)
