from django.urls import path

from apps.company.api.views import OwnerApplications, OwnerCreateView, ConfirmOwners

urlpatterns = [
    path('create/owner/', OwnerCreateView.as_view()),
    path('list/owner/is_false/', OwnerApplications.as_view()),
    path('confirn/owners/', ConfirmOwners.as_view()),
]
