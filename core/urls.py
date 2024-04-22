from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("blocks.urls")),
    path("color-styles/", include("color_styles.urls")),
    path("text-styles/", include("text_styles.urls")),
    path("styles/", include("other_styles.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
