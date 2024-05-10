from django.db.models import Q
from datetime import timedelta
from decimal import Decimal


def calculate_booking_cost(room, start_date, end_date):
    property = room.hotel  # предполагается, что каждая комната связана со зданием
    total_rooms = property.hotel_rooms.count()  # общее количество комнат в здании
    daily_rate = room.price_per_night

    total_cost = 0
    current_date = start_date
    while current_date < end_date:
        applicable_rate = float(daily_rate)

        # Определение загруженности здания
        occupied_rooms = property.hotel_rooms.filter(
            bookings__start_date__lte=current_date,
            bookings__end_date__gte=current_date,
            bookings__status='confirmed'
        ).count()

        demand_percent = (float((occupied_rooms / total_rooms)) *
                          ((float(property.procent) / 100) * float(room.price_per_night)))

        print(demand_percent)

        # Применение динамической наценки за загруженность
        applicable_rate += float(demand_percent)
        print('Загруженность')
        print(applicable_rate)

        # Проверяем горячие периоды
        hot_periods = property.hot_periods.filter(
            Q(date_start__lte=current_date) & Q(date_end__gte=current_date)
        )
        for period in hot_periods:
            applicable_rate += float(period.multiply) / 100 * float(room.price_per_night)
            applicable_rate += period.surcharge

        cold_periods = property.cold_periods.filter(
            Q(date_start__lte=current_date) & Q(date_end__gte=current_date)
        )
        for period in cold_periods:
            applicable_rate *= (1 - (period.discount / 100))
        # print('Холодные')
        # print(applicable_rate)
        total_cost += applicable_rate
        current_date += timedelta(days=1)

    return total_cost

