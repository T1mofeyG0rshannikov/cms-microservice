from django.urls import path

from .views import GetProducts

urlpatterns = [path("products", GetProducts.as_view())]
