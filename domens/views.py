from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from domens.forms import CreateSiteForm
from domens.models import Domain, Site
from user.auth.jwt_processor import get_jwt_processor
from user.models import User
from utils.errors import UserErrors


@method_decorator(csrf_exempt, name="dispatch")
class CreateSite(TemplateView):
    template_name = "domens/create_site.html"

    def __init__(self):
        super().__init__()
        self.jwt_processor = get_jwt_processor()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateSiteForm()

        return context

    def post(self, request):
        form = CreateSiteForm(request.POST, request.FILES)

        token = request.headers.get("Authorization")
        payload = self.jwt_processor.validate_token(token)
        print(token, payload)
        if payload:
            user = User.objects.get_user_by_id(id=payload["id"])
        else:
            user = None

        print(user)
        print(request.user)
        print(request.user.is_authenticated)
        if user:
            # user = request.user

            try:
                if user.site is not None:
                    form.add_error("subdomain", UserErrors.you_already_have_your_own_website.value)
                    return JsonResponse({"errors": form.errors}, status=400)
            except User.site.RelatedObjectDoesNotExist:
                pass

            if form.is_valid():
                domain = Domain.objects.filter(is_partners=True).first()
                data = form.cleaned_data
                data["user"] = user
                data["is_active"] = True
                data["domain"] = domain

                Site.objects.create(**data)

                return HttpResponse(status=200)

            else:
                return JsonResponse({"errors": form.errors}, status=400)
        else:
            form.add_error("subdomain", UserErrors.login_first.value)
            return JsonResponse({"errors": form.errors}, status=400)
