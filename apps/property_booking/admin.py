from django.contrib import admin
from apps.property_booking.models import Record


@admin.register(Record)
class BookingAdmin(admin.ModelAdmin):
    pass
