from django_filters import rest_framework as filters
from django.db.models import F

from apps.property_booking.models import Booking
from apps.property.models import Property


class PropertyFilter(filters.FilterSet):
    location = filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()
    adults = filters.NumberFilter(method='filter_by_adults')
    children = filters.NumberFilter(method='filter_by_children')
    children_ages = filters.CharFilter(method='filter_by_children_ages')
    hotel_amenities = filters.CharFilter(method='filter_by_hotel_amenities')
    room_amenities = filters.CharFilter(method='filter_by_room_amenities')
    star_rating = filters.CharFilter(method='filter_by_star_rating')
    hotel_brands = filters.CharFilter(method='filter_by_hotel_brands')

    class Meta:
        model = Property
        fields = ['location', 'date_start', 'date_end', 'adults', 'children',
                  'children_ages', 'hotel_amenities', 'room_amenities', 'star_rating', 'hotel_brands']

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

    def filter_by_adults(self, queryset, name, value):
        return queryset.filter(hotel_rooms__max_adults__gte=value).distinct()

    def filter_by_children(self, queryset, name, value):
        return queryset.filter(hotel_rooms__max_children__gte=value).distinct()

    def filter_by_children_ages(self, queryset, name, value):
        ages = value.split(',')
        try:
            ages = [int(age) for age in ages]
        except ValueError:
            return queryset.none()

        return queryset.filter(hotel_rooms__max_children__gte=len(ages)).distinct()

    def filter_by_hotel_amenities(self, queryset, name, value):
        amenities = value.split(',')
        for amenity in amenities:
            queryset = queryset.filter(amenities__name=amenity)
        return queryset

    def filter_by_room_amenities(self, queryset, name, value):
        amenities = value.split(',')
        for amenity in amenities:
            queryset = queryset.filter(hotel_rooms__amenities__name=amenity)
        return queryset

    def filter_by_star_rating(self, queryset, name, value):
        star_ratings = value.split(',')
        star_ratings = [int(rating) for rating in star_ratings]
        queryset = queryset.filter(star_rating__in=star_ratings)
        return queryset

    def filter_by_hotel_brands(self, queryset, name, value):
        brands = value.split(',')
        queryset = queryset.filter(brand__in=brands)
        return queryset
