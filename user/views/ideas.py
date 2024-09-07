from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from common.views import FormView
from user.forms import AddIdeaForm
from user.idea_service.idea_service import get_idea_service
from user.models.idea import Idea, IdeaScreen, Like
from user.usecases.get_ideas import GetIdeas
from user.views.base_user_view import APIUserRequired


@method_decorator(csrf_exempt, name="dispatch")
class LikeView(APIUserRequired):
    def get_idea(self):
        idea = self.request.GET.get("idea")

        try:
            return Idea.objects.get(id=idea)
        except Idea.DoesNotExist:
            return None

    def post(self, request):
        user = request.user
        idea = self.get_idea()

        if not idea:
            return HttpResponse(status=404)

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
        print(request.POST, request.FILES)
        idea = Idea.objects.create(
            title=form.cleaned_data.get("title"),
            description=form.cleaned_data.get("description"),
            category=form.cleaned_data.get("category"),
            user=request.user,
        )

        screens = request.FILES.getlist("screens")

        for screen in screens:
            IdeaScreen.objects.create(screen=screen, idea=idea)

        return HttpResponse(status=201)


class GetIdeasView(APIUserRequired):
    get_ideas_interactor = GetIdeas(get_idea_service())

    def get(self, request):
        filter = self.request.GET.get("category")
        sorted_by = self.request.GET.get("sorted_by")
        status = self.request.GET.get("status")

        user = request.user

        return JsonResponse({"ideas": self.get_ideas_interactor(filter, sorted_by, status, user)})
