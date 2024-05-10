from django.db.models import Q

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from apps.property_booking.models import Record
from apps.property.models import Room
from api.property_booking.serializers import RecordSerializer
from django.shortcuts import get_object_or_404

from .utils import calculate_booking_cost


class RecordListCreateView(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        room = get_object_or_404(Room, pk=serializer.validated_data.get('room'))
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        cost = calculate_booking_cost(room, start_date, end_date)
        record = Record.objects.create(room=room, total_cost=cost, start_date=start_date, end_date=end_date)
        return Response(status=status.HTTP_200_OK)


class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

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


class CheckPriceRecordView(generics.GenericAPIView):
    serializer_class = RecordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room = serializer.validated_data['room']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        if start_date >= end_date:
            return Response({'detail': {
                'start_date': _("Start date must be before end date."),
                'end_date': _("End date must be after start date.")
            }}, status=status.HTTP_400_BAD_REQUEST)
        overlapping_bookings = Record.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date),
            room=room,
            status='confirmed',
        )
        if overlapping_bookings.exists():
            return Response({'detail': 'This room is already booked during the requested date range.'})
        cost = calculate_booking_cost(room, start_date, end_date)
        return Response(cost, status=status.HTTP_200_OK)
