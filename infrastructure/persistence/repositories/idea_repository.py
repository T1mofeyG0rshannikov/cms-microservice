from collections.abc import Iterable

from django.db.models import Count, F, Q, Value
from django.db.models.functions import Length, Reverse, StrIndex, Substr

from domain.common.screen import ScreenInterface
from domain.user.idea import IdeaInterface
from domain.user.idea_repository import IdeaRepositoryInterface
from infrastructure.persistence.models.user.idea import Idea, IdeaScreen, Like


class IdeaRepository(IdeaRepositoryInterface):
    def update(self, id: int, **kwargs) -> None:
        Idea.objects.filter(id=id).update(**kwargs)

    def create(self, screens: Iterable[ScreenInterface], **kwargs) -> IdeaInterface:
        idea = Idea.objects.create(**kwargs)

        for screen in screens:
            IdeaScreen.objects.create(screen=screen, idea=idea)

        return idea

    def delete(self, id: int) -> None:
        Idea.objects.get(id=id).delete()

    def get(self, id: int) -> IdeaInterface:
        try:
            return Idea.objects.get(id=id)
        except Idea.DoesNotExist:
            return None

    def get_ideas(self, category=None, sorted_by=None, status=None, user_id: int = None) -> Iterable[IdeaInterface]:
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

    def get_screens(self, idea_id: int) -> Iterable[ScreenInterface]:
        return IdeaScreen.objects.filter(idea_id=idea_id)

    def get_screen_names(self, idea_id: int) -> list[str]:
        return (
            IdeaScreen.objects.filter(idea_id=idea_id)
            .annotate(
                length=Length("screen"),
                file_name=Substr("screen", F("length") - StrIndex(Reverse(F("screen")), Value("/")) + 2, F("length")),
            )
            .values_list("file_name", flat=True)
        )

    def delete_screens(self, idea_id: int, old_screens: list[str]) -> None:
        IdeaScreen.objects.filter(idea_id=idea_id).annotate(
            length=Length("screen"),
            file_name=Substr("screen", F("length") - StrIndex(Reverse(F("screen")), Value("/")) + 2, F("length")),
        ).exclude(file_name__in=old_screens).delete()

    def create_screen(self, **kwargs) -> None:
        IdeaScreen.objects.create(**kwargs)

    def like_exists(self, user_id: int, idea_id: int) -> bool:
        return Like.objects.filter(user_id=user_id, idea_id=idea_id).exists()

    def create_like(self, user_id: int, idea_id: int) -> None:
        Like.objects.create(user_id=user_id, idea_id=idea_id)

    def delete_like(self, user_id: int, idea_id: int) -> None:
        Like.objects.filter(user_id=user_id, idea_id=idea_id).delete()


def get_idea_repository() -> IdeaRepositoryInterface:
    return IdeaRepository()
