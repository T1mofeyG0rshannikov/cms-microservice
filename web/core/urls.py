from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from web.template.views.views import PageNotFound

urlpatterns = [
    path("styles/", include("styles.urls")),
    path("user/", include("user.urls")),
    path("email/", include("emails.urls")),
    path("admin/", include("admin.urls")),
    path("komutan/", admin.site.urls),
    path("domain/", include("domens.urls")),
    path("notifications/", include("notifications.urls")),
    path("materials/", include("materials.urls")),
    path("", include("common.urls")),
    path("", include("account.urls")),
    path("", include("catalog.urls")),
    path("", include("blocks.urls")),
    path("", include("template.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r"^.*", PageNotFound.as_view())]
