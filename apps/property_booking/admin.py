from django.contrib import admin
from apps.property_booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
