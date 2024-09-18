from common.pagination import Pagination
from common.views import FormView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from user.forms import AddIdeaForm
from user.serializers import IdeasSerializer
from user.views.base_user_view import APIUserRequired
from utils.valid_images import valid_screens_size

from application.usecases.ideas.add_idea import AddIdea
from application.usecases.ideas.add_like import AddLike
from application.usecases.ideas.delete_idea import DeleteIdea
from application.usecases.ideas.get_ideas import GetIdeas
from application.usecases.ideas.remove_like import RemoveLike
from application.usecases.ideas.update_idea import UpdateIdea
from domain.user.exceptions import CantAddLike, IdeaNotFound, LikeAlreadyExists
from infrastructure.persistence.repositories.idea_repository import get_idea_repository


@method_decorator(csrf_exempt, name="dispatch")
class LikeView(APIUserRequired):
    add_like_interactor = AddLike(get_idea_repository())
    remove_like_interactor = RemoveLike(get_idea_repository())

    def post(self, request):
        user = request.user
        idea = self.request.GET.get("idea")

        try:
            self.add_like_interactor(idea, user)
        except (CantAddLike, LikeAlreadyExists) as e:
            return JsonResponse({"message": str(e)}, status=400)
        except IdeaNotFound as e:
            return JsonResponse({"message": str(e)}, status=404)

        return HttpResponse(status=201)

    def delete(self, request):
        user = request.user
        idea = self.request.GET.get("idea")

        try:
            self.remove_like_interactor(idea, user)
        except IdeaNotFound as e:
            return JsonResponse({"message": str(e)}, status=404)

        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name="dispatch")
class AddIdeaView(APIUserRequired, FormView):
    form_class = AddIdeaForm
    add_idea_interactor = AddIdea(get_idea_repository())

    def form_valid(self, request, form):
        screens = request.FILES.getlist("screens")

        errors = valid_screens_size(screens, 1_048_576, "Изображение должно быть не более 1Mb")

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        self.add_idea_interactor({**form.cleaned_data, "user": request.user}, screens)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateIdeaView(APIUserRequired, FormView):
    form_class = AddIdeaForm
    update_idea_intercator = UpdateIdea(get_idea_repository())

    def form_valid(self, request, form):
        idea = request.GET.get("idea")

        screens = request.FILES.getlist("screens")
        old_screens = request.POST.get("screensSrc").split(",")

        errors = valid_screens_size(screens, 1_048_576, "Изображение должно быть не более 1Mb")

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        self.update_idea_intercator(idea_id=idea, screens=screens, old_screens=old_screens, fields=form.cleaned_data)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteIdeaView(APIUserRequired):
    delete_idea_interactor = DeleteIdea(get_idea_repository())

    def delete(self, request):
        idea = request.GET.get("idea")
        user = request.user

        try:
            self.delete_idea_interactor(idea, user)
        except IdeaNotFound as e:
            return JsonResponse({"message": str(e)})

        return HttpResponse(status=204)


class GetIdeasView(APIUserRequired):
    get_ideas_interactor = GetIdeas(get_idea_repository())

    def get(self, request):
        filter = self.request.GET.get("category")
        sorted_by = self.request.GET.get("sorted_by")
        status = self.request.GET.get("status")

        user = request.user
        paginator = Pagination(request)

        return JsonResponse(
            paginator.paginate(
                objects=self.get_ideas_interactor(filter, sorted_by, status, user),
                objects_context_name="ideas",
                serializer_class=IdeasSerializer,
                serializer_context={"user": user},
            )
            | {"user_id": user.id}
        )
