from django.urls import path

from web.site_statistics.views import (
    OpenedProductLinkView,
    OpenedProductPopupView,
    OpenedProductPromoView,
)

urlpatterns = [
    path("opened-product-popup", OpenedProductPopupView.as_view()),
    path("opened-product-link", OpenedProductLinkView.as_view()),
    path("opened-product-promo", OpenedProductPromoView.as_view()),
]
