from django.db.models import Count, Q

from user.idea_repository.repository_interface import IdeaRepositoryInterface
from user.models.idea import Idea


class IdeaRepository(IdeaRepositoryInterface):
    @staticmethod
    def get_idea(id: int):
        try:
            return Idea.objects.get(id=id)
        except Idea.DoesNotExist:
            return None

    @staticmethod
    def get_ideas(category=None, sorted_by=None, status=None, user=None):
        filters = Q()

        if user:
            filters &= Q(user=user)

        if category:
            filters &= Q(category=category)

        if status:
            filters &= Q(status=status)

        if not sorted_by:
            sorted_by = "-id"

        return (
            Idea.objects.annotate(likes_count=Count("likes"))
            .prefetch_related("likes")
            .select_related("user")
            .filter(filters)
            .order_by(sorted_by)
        )


def get_idea_repository() -> IdeaRepository:
    return IdeaRepository()
