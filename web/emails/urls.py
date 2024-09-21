from django.urls import path

from web.emails.views import SendAdminAuthCode, SendConfirmEmail

urlpatterns = [
    path("send-confirm-email", SendConfirmEmail.as_view()),
    path("send-auth-admin-code", SendAdminAuthCode.as_view()),
]
