from django.contrib import admin
from apps.property_booking.models import Record, HotPeriod, ColdPeriod


@admin.register(Record)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(HotPeriod)
class HotPeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(ColdPeriod)
class ColdPeriodAdmin(admin.ModelAdmin):
    pass
