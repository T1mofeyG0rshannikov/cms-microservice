from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from common.models import SocialNetwork


class SiteView(LoginRequiredMixin, TemplateView):
    login_url = "/user/login"
    template_name = "account/site.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["socials"] = SocialNetwork.objects.all()

        return context
