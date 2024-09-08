from user.idea_service.idea_service_interface import IdeaServiceInterface


class GetIdeas:
    def __init__(self, service: IdeaServiceInterface):
        self.service = service

    def __call__(self, category, sorted_by, status, user, paginator):
        return paginator.paginate(self.service.get_ideas(category, sorted_by, status, user), "ideas")
