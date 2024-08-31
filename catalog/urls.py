from django.urls import path

from .views import GetProducts, GetUserProducts

urlpatterns = [
    path("products", GetProducts.as_view()),
    path("user-products", GetUserProducts.as_view()),
]
