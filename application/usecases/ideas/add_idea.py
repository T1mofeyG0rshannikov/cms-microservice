from collections.abc import Iterable
from dataclasses import dataclass

from application.texts.errors import ErrorsMessages
from domain.common.screen import ScreenInterface
from domain.common.valid_images import valid_screens_size
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


@dataclass
class AddIdeaResponse:
    errors: dict[str, str] = None


class AddIdea:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, screens: Iterable[ScreenInterface], **kwargs) -> AddIdeaResponse:
        errors = valid_screens_size(screens, 1_048_576, ErrorsMessages.to_large_file_1mb)

        if errors:
            return AddIdeaResponse(errors=errors)

        self.repository.create(**kwargs, screens=screens)
        return AddIdeaResponse()


def get_add_idea_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> AddIdea:
    return AddIdea(idea_repository)
