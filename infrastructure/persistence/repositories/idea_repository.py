from typing import Any

from django.db.models import Count, Q

from domain.user.idea_repository_interface import IdeaRepositoryInterface
from web.user.models.idea import Idea, IdeaScreen, Like


class IdeaRepository(IdeaRepositoryInterface):
    @staticmethod
    def update_idea(id: int, fields: dict[str, str]) -> None:
        Idea.objects.filter(id=id).update(**fields)

    @staticmethod
    def create_idea(fields: dict[str, str], screens) -> Idea:
        idea = Idea.objects.create(**fields)

        for screen in screens:
            IdeaScreen.objects.create(screen=screen, idea=idea)

        return idea

    @staticmethod
    def delete_idea(id: int) -> None:
        Idea.objects.filter(id=id).delete()

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

    @staticmethod
    def get_screens(idea_id: int) -> list[Idea]:
        return IdeaScreen.objects.filter(idea_id=idea_id)

    def get_screen_names(self, idea_id: int) -> list[str]:
        return self.get_screens(idea_id).values_list("screen", flat=True)

    @staticmethod
    def delete_screens(idea_id: int, old_screens: list[str]) -> None:
        for screen in IdeaScreen.objects.filter(idea_id=idea_id):
            if screen.screen.name.split("/")[-1] not in old_screens:
                screen.delete()

    @staticmethod
    def create_screen(fields: dict[str, Any]) -> None:
        IdeaScreen.objects.create(**fields)

    @staticmethod
    def like_exists(user_id: int, idea_id: int) -> bool:
        return Like.objects.filter(user_id=user_id, idea_id=idea_id).exists()

    @staticmethod
    def create_like(user_id: int, idea_id: int) -> None:
        Like.objects.create(user_id=user_id, idea_id=idea_id)

    @staticmethod
    def delete_like(user_id: int, idea_id: int) -> None:
        Like.objects.filter(user_id=user_id, idea_id=idea_id).delete()


def get_idea_repository() -> IdeaRepository:
    return IdeaRepository()
