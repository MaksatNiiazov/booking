from django.urls import path

from apps.property.api.views import (
    AddressListCreateView,
    AddressDetailView,
    AmenityListCreateView,
    AmenityDetailView,
    PropertyListCreateView,
    PropertyDetailView,
    RoomListCreateView,
    RoomDetailView,
    ReviewListCreateView,
    ReviewRetrieveUpdateDestroyView
)

urlpatterns = [
    path('addresses/', AddressListCreateView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('amenities/', AmenityListCreateView.as_view(), name='amenity-list'),
    path('amenities/<int:pk>/', AmenityDetailView.as_view(), name='amenity-detail'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]
