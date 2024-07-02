from django.urls import path

from .views import SiteView

urlpatterns = [
    path("site", SiteView.as_view()),
    # path("<slug>", slug_router),
    # path("templates/get", ShowTemplates.as_view()),
    #  path("page/clone", ClonePage.as_view()),
]
