from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class SiteView(LoginRequiredMixin, TemplateView):
    login_url = "/user/login"
    template_name = "account/site.html"
