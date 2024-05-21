from django.contrib import admin

# Register your models here.
from apps.property_crm.models import ExpenseCategory, IncomeCategory, Expense, Income, Booking, RoomServiceUsage


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomServiceUsage)
class RoomServiceUsageAdmin(admin.ModelAdmin):
    list_display = ('room', 'service', 'date_used', 'price')
    list_filter = ('room', 'service', 'date_used')
    search_fields = ('room__room_number', 'service__name')



class RoomProfitabilityAdmin(admin.ModelAdmin):
    list_display = (
        'room', 'date_start', 'date_end', 'total_income', 'total_service_income', 'total_expenses', 'net_profit')
    list_filter = ('room', 'date_start', 'date_end')
    search_fields = ('room__room_number',)


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'description')
    list_filter = ('category', 'date')
    search_fields = ('category__name', 'description')


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'description')
    list_filter = ('category', 'date')
    search_fields = ('category__name', 'description')
