from django.urls import path

from .views import ClonePage, ShowCatalogPage, ShowPage, ShowTemplates, slug_router

urlpatterns = [
    path("<slug>", slug_router),
    # path("<products_slug>", slug_router, name="catalog_page"),
    path("templates/get", ShowTemplates.as_view()),
    path("page/clone", ClonePage.as_view()),
]
