from django.urls import path

from .views import ChangeSiteView, SiteView

urlpatterns = [path("site", SiteView.as_view()), path("change-site", ChangeSiteView.as_view())]
