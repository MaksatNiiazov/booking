from django.urls import path

from apps.property_crm.api import views

urlpatterns = [
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<uuid:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
]
