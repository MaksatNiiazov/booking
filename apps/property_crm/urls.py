from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.property_crm.api.urls'))

]
