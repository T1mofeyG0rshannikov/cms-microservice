from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from common.pagination import Pagination
from common.views import FormView
from user.forms import AddIdeaForm
from user.idea_repository.repository import get_idea_repository
from user.idea_service.idea_service import get_idea_service
from user.models.idea import Idea, IdeaScreen, Like
from user.usecases.get_ideas import GetIdeas
from user.views.base_user_view import APIUserRequired


@method_decorator(csrf_exempt, name="dispatch")
class LikeView(APIUserRequired):
    repository = get_idea_repository()

    def get_idea(self):
        idea = self.request.GET.get("idea")

        return self.repository.get_idea(idea)

    def post(self, request):
        user = request.user
        idea = self.get_idea()

        if not idea:
            return HttpResponse(status=404)

        if idea.user == user:
            return JsonResponse({"message": "You cant like your own ideas"}, status=400)

        if Like.objects.filter(user=user, idea=idea).exists():
            return JsonResponse({"message": "You already had liked this idea"}, status=400)

        Like.objects.create(user=user, idea=idea)

        return HttpResponse(status=201)

    def delete(self, request):
        user = request.user
        idea = self.get_idea()
        if not idea:
            return HttpResponse(status=404)

        Like.objects.filter(user=user, idea=idea).delete()

        return HttpResponse(status=204)


class DeleteIdea(APIUserRequired):
    def delete(self, request):
        user = request.user
        idea = QueryDict(request.body).get("idea")

        Idea.objects.filter(user=user, idea_id=idea).delete()

        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name="dispatch")
class AddIdea(APIUserRequired, FormView):
    form_class = AddIdeaForm

    def form_valid(self, request, form):
        screens = request.FILES.getlist("screens")

        errors = {}
        for i, screen in enumerate(screens):
            if screen.size > 1_048_576:
                errors[f"file{i + 1}"] = ["Изображение должно быть не более 1Mb"]

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        idea = Idea.objects.create(
            title=form.cleaned_data.get("title"),
            description=form.cleaned_data.get("description"),
            category=form.cleaned_data.get("category"),
            user=request.user,
        )

        for screen in screens:
            IdeaScreen.objects.create(screen=screen, idea=idea)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateIdea(APIUserRequired, FormView):
    form_class = AddIdeaForm

    def form_valid(self, request, form):
        idea_id = request.GET.get("idea")

        idea = Idea.objects.get(id=idea_id)

        screens = request.FILES.getlist("screens")
        screensSrc = request.POST.get("screensSrc").split(",")
        currentScreensSrc = [screen.screen.name.split("/")[-1] for screen in idea.screens.all()]

        print(screens)
        print(screensSrc)
        print(currentScreensSrc)

        errors = {}
        for i, screen in enumerate(screens):
            if screen.size > 1_048_576:
                errors[f"file{i + 1}"] = ["Изображение должно быть не более 1Mb"]

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        idea.title = form.cleaned_data.get("title")
        idea.description = form.cleaned_data.get("description")
        idea.category = form.cleaned_data.get("category")

        idea.save()

        for screen in idea.screens.all():
            print(screen.screen.name.split("/")[-1], "name2")
            if screen.screen.name.split("/")[-1] not in screensSrc:
                screen.delete()

        for screen in screens:
            print(screen.name, "name1")
            if screen.name not in currentScreensSrc:
                IdeaScreen.objects.create(screen=screen, idea=idea)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteIdeaView(APIUserRequired):
    def delete(self, request):
        idea = request.GET.get("idea")

        print(idea, type(idea))
        print(Idea.objects.filter(user=request.user, id=idea))

        Idea.objects.filter(user=request.user, id=idea).delete()
        return HttpResponse(status=204)


class GetIdeasView(APIUserRequired):
    get_ideas_interactor = GetIdeas(get_idea_service())

    def get(self, request):
        filter = self.request.GET.get("category")
        sorted_by = self.request.GET.get("sorted_by")
        status = self.request.GET.get("status")

        user = request.user
        paginator = Pagination(request)

        return JsonResponse(self.get_ideas_interactor(filter, sorted_by, status, user, paginator))
