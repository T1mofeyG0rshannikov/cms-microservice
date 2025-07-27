from django.urls import path

from .views import GetOrganizationsView, GetProductCategoriesView, GetProductsView

urlpatterns = [
    path("api/product-categories", GetProductCategoriesView.as_view()),
    path("api/products", GetProductsView.as_view()),
    path("api/organizations", GetOrganizationsView.as_view()),
]
