from domain.user.idea_repository import IdeaRepositoryInterface


class GetIdeas:
    def __init__(self, repository: IdeaRepositoryInterface):
        self.repository = repository

    def __call__(self, filter, sorted_by, status, user):
        idea_user = None
        category = None

        if filter == "my":
            idea_user = user

        elif filter:
            category = filter

        return self.repository.get_ideas(category=category, user=idea_user, status=status, sorted_by=sorted_by)
