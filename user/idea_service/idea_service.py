from user.idea_repository.repository import get_idea_repository
from user.idea_repository.repository_interface import IdeaRepositoryInterface
from user.idea_service.idea_service_interface import IdeaServiceInterface
from user.interfaces import UserInterface
from user.serializers import IdeasSerializer


class IdeaService(IdeaServiceInterface):
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def get_ideas(self, filter: str, sorted_by: str, status: str, user: UserInterface):
        idea_user = None
        category = None

        if filter == "my":
            idea_user = user

        elif filter:
            category = filter

        ideas = self.repository.get_ideas(category=category, user=idea_user, status=status, sorted_by=sorted_by)

        return IdeasSerializer(ideas, context={"user": user}, many=True).data


def get_idea_service() -> IdeaService:
    return IdeaService(get_idea_repository())
