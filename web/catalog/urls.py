from django.urls import path

from .views import (
    GetOrganizationsView,
    GetProductCategoriesView,
    GetProductsView,
    GetProductView,
)

urlpatterns = [
    path("api/product-categories", GetProductCategoriesView.as_view()),
    path("api/products", GetProductsView.as_view()),
    path("api/product/<int:product_id>", GetProductView.as_view()),
    path("api/organizations", GetOrganizationsView.as_view()),
]
