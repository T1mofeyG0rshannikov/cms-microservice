from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


@method_decorator(csrf_exempt, name="dispatch")
class JoomlaAdminPage(TemplateView):
    template_name = "admin/joomla.html"

    def post(self, request):
        print(request.POST)
        password = request.POST.get("passwd")
        if not password:
            return render(request, "admin/joomla.html", {"error": "Empty password not allowed"})

        return render(
            request,
            "admin/joomla.html",
            {"error": "Username and password do not match or you do not have an account yet."},
        )
