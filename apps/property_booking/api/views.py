from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.property_booking.models import Booking
from apps.property_booking.api.serializers import BookingSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        date_start = serializer.validated_data['date_start']
        date_end = serializer.validated_data['date_end']

        total_price = room.default_price_per_night * (date_end - date_start).days

        serializer.save(user=self.request.user, total_price=total_price)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        booking = self.get_object()
        if booking.user != self.request.user:
            return Response({'error': 'You do not have permission to edit this booking.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response({'error': 'You do not have permission to delete this booking.'},
                            status=status.HTTP_403_FORBIDDEN)
        instance.delete()
