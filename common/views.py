from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from common.security import LinkEncryptor


class RedirectToLink(View):
    link_encryptor = LinkEncryptor()

    def get(self, request):
        tracker = self.request.GET.get("product")
        print(tracker, "gfdgdddg")
        if tracker:
            link = self.link_encryptor.decrypt(tracker)
            print(link)
            if link:
                return HttpResponseRedirect(link)

        return HttpResponse(status=400)
