from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.accounts.api.urls'))

]
