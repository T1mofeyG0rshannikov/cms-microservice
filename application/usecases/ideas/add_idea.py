from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class AddIdea:
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def __call__(self, fields: dict[str, str], screens) -> None:
        self.repository.create_idea(fields, screens)


def get_add_idea_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> AddIdea:
    return AddIdea(idea_repository)
