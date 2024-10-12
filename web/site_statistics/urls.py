from django.urls import path

from web.site_statistics.views import (
    IncrementBanksCountView,
    OpenedChangePasswordFormView,
    OpenedProductLinkView,
    OpenedProductPopupView,
    OpenedProductPromoView,
    OpenedUpdateProductFormView,
    SubmitCapcha,
)

urlpatterns = [
    path("opened-product-popup", OpenedProductPopupView.as_view()),
    path("opened-product-link", OpenedProductLinkView.as_view()),
    path("opened-product-promo", OpenedProductPromoView.as_view()),
    path("opened-change-password-form", OpenedChangePasswordFormView.as_view()),
    path("opened-update-user-form", OpenedUpdateProductFormView.as_view()),
    path("increment-banks-count", IncrementBanksCountView.as_view()),
    path("submit-capcha", SubmitCapcha.as_view()),
]
