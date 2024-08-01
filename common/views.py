import re

from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, View

from common.security import LinkEncryptor
from common.template_loader.template_loader import get_template_loader
from domens.get_domain import get_domain_string, get_partners_domain_string
from domens.models import Domain, Site
from settings.get_settings import get_settings
from settings.models import SiteSettings

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from domens.models import Site
from settings.models import SiteSettings

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from domens.models import Site
from settings.models import SiteSettings


class RedirectToLink(View):
    link_encryptor = LinkEncryptor()

    def get(self, request):
        tracker = self.request.GET.get("product")
        if tracker:
            link = self.link_encryptor.decrypt(tracker)

            if link:
                return HttpResponseRedirect(link)

        return HttpResponse(status=400)


class GetChangeUserFormTemplate(View):
    template_loader = get_template_loader()
    
    def get(self, request):
        template = self.template_loader.load_change_user_form(request)
        return JsonResponse({"content": template})


class GetChangeSiteFormTemplate(View):
    template_loader = get_template_loader()
    
    def get(self, request):
        template = self.template_loader.load_change_site_form(request)
        return JsonResponse({"content": template})


class SettingsMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        settings = get_settings(self.request.domain, self.request.subdomain)

        if self.request.domain == "localhost":
            domain = "localhost:8000"
        else:
            domain = get_domain_string()

        partner_domain = get_partners_domain_string()

        context["settings"] = settings
        context["domain"] = domain
        context["partner_domain"] = partner_domain

        return context


class SubdomainMixin(SettingsMixin):
    def get_domain(self, request):
        host = request.get_host()
        host = host.replace("127.0.0.1", "localhost")
        if ":" in host:
            host = host.split(":")[0]

        subdomain = self.get_subdomain(request)
        first_domain = host.split(".")[-1]

        domain = re.findall(f"{subdomain}.*?{first_domain}", host)[0]
        domain = re.sub(subdomain, "", domain)
        if domain[0] == ".":
            domain = domain[1::]

        return domain

    def get_subdomain(self, request):
        host = request.get_host()
        host = host.replace("127.0.0.1", "localhost")

        if "localhost" in host:
            if "." not in host:
                return ""

            return host.split(".")[0]

        if host.count(".") < 2:
            return ""

        return host.split(".")[0]

    def valid_subdomain(self, subdomain: str) -> bool:
        if not subdomain:
            return True

        if Site.objects.filter(subdomain=subdomain).exists() and Site.objects.get(subdomain=subdomain).is_active:
            return True

        if subdomain == "www":
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        subdomain = self.get_subdomain(request)
        domain = self.get_domain(request)

        if not self.valid_subdomain(subdomain):
            return HttpResponseNotFound("404 Subdomen not found")

        if (
            domain != "localhost"
            and subdomain
            and not Site.objects.filter(Q(domain__domain=domain) & Q(subdomain=subdomain)).exists()
        ):
            return HttpResponseNotFound("404 Subdomen not found")

        if Domain.objects.filter(is_partners=True).exists():
            partner_domain = get_partners_domain_string()

            if domain == partner_domain and not subdomain and request.path != "":
                return HttpResponseNotFound("404 Page not found")

            if domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
                return HttpResponseRedirect("/")

            if request.path.startswith("/admin/") and partner_domain in request.get_host():
                return HttpResponseNotFound("404 Page not found")

        request.domain = domain
        request.subdomain = subdomain

        return super().dispatch(request, *args, **kwargs)
