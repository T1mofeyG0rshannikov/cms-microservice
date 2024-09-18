from domain.user.idea_repository_interface import IdeaRepositoryInterface


class AddIdea:
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def __call__(self, fields: dict[str, str], screens) -> None:
        self.repository.create_idea(fields, screens)
