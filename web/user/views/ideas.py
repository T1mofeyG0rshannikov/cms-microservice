from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from application.texts.errors import ErrorsMessages
from application.usecases.ideas.add_idea import AddIdea, get_add_idea_interactor
from application.usecases.ideas.add_like import AddLike, get_add_like_interactor
from application.usecases.ideas.delete_idea import (
    DeleteIdea,
    get_delete_idea_interactor,
)
from application.usecases.ideas.get_ideas import GetIdeas, get_get_ideas_interactor
from application.usecases.ideas.remove_like import (
    RemoveLike,
    get_remove_like_interactor,
)
from application.usecases.ideas.update_idea import (
    UpdateIdea,
    get_update_idea_interactor,
)
from domain.common.valid_images import valid_screens_size
from domain.user.exceptions import CantAddLike, IdeaNotFound, LikeAlreadyExists
from web.common.pagination import Pagination
from web.common.views import FormView
from web.user.forms import AddIdeaForm
from web.user.serializers import IdeasSerializer
from web.user.views.base_user_view import APIUserRequired


@method_decorator(csrf_exempt, name="dispatch")
class LikeView(APIUserRequired):
    add_like_interactor: AddLike = get_add_like_interactor()
    remove_like_interactor: RemoveLike = get_remove_like_interactor()

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        idea = self.request.GET.get("idea")

        try:
            self.add_like_interactor(idea, user.id)
        except (CantAddLike, LikeAlreadyExists) as e:
            return JsonResponse({"message": str(e)}, status=400)
        except IdeaNotFound as e:
            return JsonResponse({"message": str(e)}, status=404)

        return HttpResponse(status=201)

    def delete(self, request: HttpRequest) -> HttpResponse:
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
    add_idea_interactor: AddIdea = get_add_idea_interactor()

    def form_valid(self, request: HttpRequest, form: AddIdeaForm) -> HttpResponse:
        screens = request.FILES.getlist("screens")

        errors = valid_screens_size(screens, 1_048_576, ErrorsMessages.to_large_file_1mb)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        self.add_idea_interactor({**form.cleaned_data, "user": request.user}, screens)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateIdeaView(APIUserRequired, FormView):
    form_class = AddIdeaForm
    update_idea_intercator: UpdateIdea = get_update_idea_interactor()

    def form_valid(self, request: HttpRequest, form: AddIdeaForm) -> HttpResponse:
        idea = request.GET.get("idea")

        screens = request.FILES.getlist("screens")
        old_screens = request.POST.get("screensSrc").split(",")

        errors = valid_screens_size(screens, 1_048_576, ErrorsMessages.to_large_file_1mb)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        self.update_idea_intercator(idea_id=idea, screens=screens, old_screens=old_screens, **form.cleaned_data)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteIdeaView(APIUserRequired):
    delete_idea_interactor: DeleteIdea = get_delete_idea_interactor()

    def delete(self, request: HttpRequest) -> HttpResponse:
        idea = request.GET.get("idea")
        user = request.user

        try:
            self.delete_idea_interactor(idea, user)
        except IdeaNotFound as e:
            return JsonResponse({"message": str(e)})

        return HttpResponse(status=204)


class GetIdeasView(APIUserRequired):
    get_ideas_interactor: GetIdeas = get_get_ideas_interactor()

    def get(self, request: HttpRequest) -> JsonResponse:
        filter = request.GET.get("category")
        sorted_by = request.GET.get("sorted_by")
        status = request.GET.get("status")

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
