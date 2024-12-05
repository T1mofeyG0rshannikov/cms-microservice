from django.urls import path

from web.common.views import RedirectToLink, SendFeedbackView

urlpatterns = [path("product", RedirectToLink.as_view()), path("feedback", SendFeedbackView.as_view())]
