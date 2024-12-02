from domain.user.idea import IdeaInterface
from domain.user.idea_repository import IdeaRepositoryInterface


class GetIdeas:
    def __init__(self, repository: IdeaRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, filter, sorted_by, status, user_id: int) -> list[IdeaInterface]:
        idea_user = None
        category = None

        if filter == "my":
            idea_user = user_id

        elif filter:
            category = filter

        return self.repository.get_ideas(category=category, user=idea_user, status=status, sorted_by=sorted_by)
