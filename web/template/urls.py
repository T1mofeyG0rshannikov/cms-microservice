from django.urls import path

from .views.views import (
    GetChangeSiteFormTemplate,
    GetChangeSocialsFormTemplate,
    GetChangeUserFormTemplate,
    GetChoiceProductForm,
    GetCreateIdeaForm,
    GetCreateUserProductForm,
    GetDeleteProductPopup,
    GetProductDescriptionPopup,
    GetReferralPopupTemplate,
    IdeasTemplate,
    ManualsTemplate,
    ProfileTemplate,
    RefsTemplate,
    SiteTemplate,
    UserProductsTemplate,
    slug_router,
)

urlpatterns = [
    path("get-change-socials-form", GetChangeSocialsFormTemplate.as_view()),
    path("get-change-site-form", GetChangeSiteFormTemplate.as_view()),
    path("get-change-user-form", GetChangeUserFormTemplate.as_view()),
    path("get-template-profile", ProfileTemplate.as_view()),
    path("get-template-manuals", ManualsTemplate.as_view()),
    path("get-template-refs", RefsTemplate.as_view()),
    path("get-template-ideas", IdeasTemplate.as_view()),
    path("get-template-products", UserProductsTemplate.as_view()),
    path("get-template-site", SiteTemplate.as_view()),
    path("get-choice-product-form", GetChoiceProductForm.as_view()),
    path("get-create-user-product-form", GetCreateUserProductForm.as_view()),
    path("get-product-description-popup", GetProductDescriptionPopup.as_view()),
    path("get-delete-product-popup", GetDeleteProductPopup.as_view()),
    path("get-referral-popup", GetReferralPopupTemplate.as_view()),
    path("get-create-idea-form", GetCreateIdeaForm.as_view()),
    path("<slug:str>", slug_router),
]
