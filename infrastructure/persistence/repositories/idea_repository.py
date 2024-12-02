from typing import Any

from django.db.models import Count, Q

from domain.user.idea import IdeaInterface
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.models.user.idea import Idea, IdeaScreen, Like


class IdeaRepository(IdeaRepositoryInterface):
    def update_idea(self, id: int, fields: dict[str, str]) -> None:
        Idea.objects.filter(id=id).update(**fields)

    def create_idea(self, fields: dict[str, str], screens) -> IdeaInterface:
        idea = Idea.objects.create(**fields)

        for screen in screens:
            IdeaScreen.objects.create(screen=screen, idea=idea)

        return idea

    def delete_idea(self, id: int) -> None:
        Idea.objects.filter(id=id).delete()

    def get_idea(self, id: int) -> IdeaInterface:
        try:
            return Idea.objects.get(id=id)
        except Idea.DoesNotExist:
            return None

    def get_ideas(self, category=None, sorted_by=None, status=None, user_id: int=None) -> list[IdeaInterface]:
        filters = Q()

        if user_id:
            filters &= Q(user_id=user_id)

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

    def get_screens(self, idea_id: int) -> list[IdeaInterface]:
        return IdeaScreen.objects.filter(idea_id=idea_id)

    def get_screen_names(self, idea_id: int) -> list[str]:
        return self.get_screens(idea_id).values_list("screen", flat=True)

    def delete_screens(self, idea_id: int, old_screens: list[str]) -> None:
        for screen in IdeaScreen.objects.filter(idea_id=idea_id):
            if screen.screen.name.split("/")[-1] not in old_screens:
                screen.delete()

    def create_screen(self, fields: dict[str, Any]) -> None:
        IdeaScreen.objects.create(**fields)

    def like_exists(self, user_id: int, idea_id: int) -> bool:
        return Like.objects.filter(user_id=user_id, idea_id=idea_id).exists()

    def create_like(self, user_id: int, idea_id: int) -> None:
        Like.objects.create(user_id=user_id, idea_id=idea_id)

    def delete_like(self, user_id: int, idea_id: int) -> None:
        Like.objects.filter(user_id=user_id, idea_id=idea_id).delete()


def get_idea_repository() -> IdeaRepositoryInterface:
    return IdeaRepository()
