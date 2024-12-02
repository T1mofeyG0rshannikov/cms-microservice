from typing import Any, Protocol

from domain.user.idea import IdeaInterface


class IdeaRepositoryInterface(Protocol):
    def delete_idea(self, id: int) -> None:
        raise NotImplementedError
    
    def create_like(self, user_id: int, idea_id: int) -> None:
        raise NotImplementedError

    def get_ideas(self, category=None, sorted_by=None, status=None, user_id: int=None) -> list[IdeaInterface]:
        raise NotImplementedError

    def get_idea(self, id: int) -> IdeaInterface:
        raise NotImplementedError
    
    def update_idea(self, idea_id: int, fields: dict[str, Any]) -> None:
        raise NotImplementedError
    
    def get_screens(self, idea_id: int):
        raise NotImplementedError
    
    def get_screen_names(self, idea_id: int) -> list[str]:
        raise NotImplementedError
    
    def create_screen(self, fields: dict[str, Any]) -> None:
        raise NotImplementedError
    
    def delete_like(self, user_id: int, idea_id: int) -> None:
        raise NotImplementedError
    
    def like_exists(self, user_id: int, idea_id: int) -> bool:
        raise NotImplementedError
    
    def create_idea(self, fields: dict[str, Any], screens) -> None:
        raise NotImplementedError
