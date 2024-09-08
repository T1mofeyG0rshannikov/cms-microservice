from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from common.security import LinkEncryptor


class RedirectToLink(View):
    link_encryptor = LinkEncryptor()

    def get(self, request):
        tracker = self.request.GET.get("product")
        if tracker:
            link = self.link_encryptor.decrypt(tracker)

            if link:
                return HttpResponseRedirect(link)

        return HttpResponse(status=400)


@method_decorator(csrf_exempt, name="dispatch")
class FormView(View):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request, form, *args, **kwargs)

        return JsonResponse({"errors": form.errors}, status=400)

    def get_form(self):
        return self.form_class(self.request.POST, self.request.FILES)
