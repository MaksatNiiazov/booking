from django_filters import rest_framework as filters

from apps.property_booking.models import Booking
from apps.property.models import Property


class PropertyFilter(filters.FilterSet):
    location = filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()
    adults = filters.NumberFilter()
    children = filters.NumberFilter()
    children_ages = filters.CharFilter()

    class Meta:
        model = Property
        fields = ['location', 'date_start', 'date_end', 'adults', 'children', 'children_ages']

    def filter_queryset(self, queryset):
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')

        if date_start and date_end:
            overlapping_bookings = Booking.objects.filter(
                date_start__lt=date_end,
                date_end__gt=date_start,
                status__in=['confirmed', 'created']
            ).values_list('room_id', flat=True)

            queryset = queryset.exclude(
                hotel_rooms__in=overlapping_bookings
            )

        return super().filter_queryset(queryset)