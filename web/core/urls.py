from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from web.template.views.views import PageNotFound

urlpatterns = [
    path("styles/", include("web.styles.urls")),
    path("user/", include("web.user.urls")),
    path("email/", include("web.emails.urls")),
    path("", include("web.admin.urls")),
    path("domain/", include("web.domens.urls")),
    path("notifications/", include("web.notifications.urls")),
    path("materials/", include("web.materials.urls")),
    path("site_statistics/", include("web.site_statistics.urls")),
    path("", include("web.common.urls")),
    path("", include("web.account.urls")),
    path("", include("web.catalog.urls")),
    path("", include("web.blocks.urls")),
    path("", include("web.template.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r"^.*", PageNotFound.as_view())]
