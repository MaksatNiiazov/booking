from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.property_booking.api.urls'))

]
