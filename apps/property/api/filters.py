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
    hotel_amenities = filters.CharFilter(method='filter_by_hotel_amenities')
    room_amenities = filters.CharFilter(method='filter_by_room_amenities')
    star_rating = filters.CharFilter(method='filter_by_star_rating')
    hotel_brands = filters.CharFilter(method='filter_by_hotel_brands')

    class Meta:
        model = Property
        fields = ['location', 'date_start', 'date_end', 'adults', 'children',
                  'children_ages', 'hotel_amenities', 'room_amenities', 'star_rating']

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
        # value может быть строкой с несколькими вариантами оценки, разделенными запятыми
        star_ratings = value.split(',')
        # Мы приводим строковые значения к числовому типу для корректной фильтрации
        star_ratings = [int(rating) for rating in star_ratings]
        # Фильтруем недвижимость по каждой оценке
        queryset = queryset.filter(star_rating__in=star_ratings)
        return queryset

    def filter_by_hotel_brands(self, queryset, name, value):
        brands = value.split(',')
        queryset = queryset.filter(brand__in=brands)
        return queryset
