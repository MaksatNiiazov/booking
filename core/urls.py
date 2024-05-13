from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("apps.accounts.urls")),
    path("company/", include("apps.company.urls")),
    path("property/", include("apps.property.urls")),
    path("property_booking/", include("apps.property_booking.urls")),
    path("docs/", include("apps.openapi.urls")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
