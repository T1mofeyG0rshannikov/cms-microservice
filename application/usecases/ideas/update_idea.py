from collections.abc import Iterable

from domain.common.screen import ScreenInterface
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


class UpdateIdea:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, idea_id: int, screens, old_screens: list[str], **kwargs) -> None:
        self.repository.delete_screens(idea_id, old_screens)
        self.create_screens(idea_id, screens)

        self.repository.update_idea(idea_id, **kwargs)

    def create_screens(self, idea_id: int, screens: Iterable[ScreenInterface]) -> None:
        current_screens = self.repository.get_screen_names(idea_id)

        for screen in screens:
            if screen.name not in current_screens:
                self.repository.create_screen(screen=screen, idea_id=idea_id)


def get_update_idea_interactor(idea_repository: IdeaRepositoryInterface = get_idea_repository()) -> UpdateIdea:
    return UpdateIdea(idea_repository)
