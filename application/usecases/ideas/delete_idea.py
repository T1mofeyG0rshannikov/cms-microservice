from domain.referrals.referral import UserInterface
from domain.user.exceptions import IdeaNotFound
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class DeleteIdea:
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def __call__(self, idea_id: int, user: UserInterface) -> None:
        idea = self.repository.get_idea(idea_id)
        if user != idea.user:
            raise IdeaNotFound(f'No idea with id "{idea_id}" written by {user}')

        self.repository.delete_idea(idea.id)


def get_delete_idea_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> DeleteIdea:
    return DeleteIdea(idea_repository)
