from typing import Any

from domain.user.idea_repository import IdeaRepositoryInterface


class UpdateIdea:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def delete_screens(self, idea_id: int, old_screens: list[str]) -> None:
        screens = self.repository.get_screens(idea_id)

        for screen in screens:
            if screen.screen.name.split("/")[-1] not in old_screens:
                screen.delete()

    def get_screen_names(self, idea_id: int):
        return [screen.split("/")[-1] for screen in self.repository.get_screen_names(idea_id)]

    def create_screens(self, idea_id: int, screens) -> None:
        current_screens = self.get_screen_names(idea_id)

        for screen in screens:
            if screen.name not in current_screens:
                self.repository.create_screen({"screen": screen, "idea_id": idea_id})

    def __call__(self, idea_id: int, screens, old_screens, fields: dict[str, Any]) -> None:
        self.delete_screens(idea_id, old_screens)
        self.create_screens(idea_id, screens)

        self.repository.update_idea(idea_id, fields)
