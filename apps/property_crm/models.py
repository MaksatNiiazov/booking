from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.property.models import Room, PaidService
from apps.common.models import CoreModel

User = get_user_model()


class Booking(CoreModel):
    STATUS_CHOICES = [
        ('created', _("Создано")),
        ('confirmed', _("Подтверждено")),
        ('cancelled', _("Отменено")),
        ('completed', _("Завершено")),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings", verbose_name=_("Комната"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Итоговая цена"))
    adults = models.IntegerField(verbose_name=_('Количество взрослых'))
    children = models.IntegerField(verbose_name=_('Количество детей'))
    children_ages = models.JSONField(verbose_name=_("Возраст детей"), blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name=_("Статус бронирования")
    )

    class Meta:
        verbose_name = _("Бронирование")
        verbose_name_plural = _("Бронирования")

    def __str__(self):
        return f"Booking by {self.user.first_name} in room {self.room.room_number} from {self.date_start} to {self.date_end}"

    def save(self, *args, **kwargs):
        if self.date_start >= self.date_end:
            raise ValueError("End date must be later than start date")

        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            date_start__lt=self.date_end,
            date_end__gt=self.date_start
        )

        if overlapping_bookings.exists():
            raise ValueError("This room is already booked during the specified period")

        super().save(*args, **kwargs)


class RoomServiceUsage(CoreModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Комната"))
    service = models.ForeignKey(PaidService, on_delete=models.CASCADE, verbose_name=_("Платная услуга"))
    date_used = models.DateField(verbose_name=_("Дата использования"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))

    class Meta:
        verbose_name = _("Использование платной услуги")
        verbose_name_plural = _("Использование платных услуг")

    def __str__(self):
        return f"{self.room.room_number} - {self.service.name} on {self.date_used}"

    def save(self, *args, **kwargs):
        # Validate that price is non-negative
        if self.price < 0:
            raise ValueError(_("Price cannot be negative"))

        super().save(*args, **kwargs)


class ExpenseCategory(CoreModel):
    """Model representing a category for expenses."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Категория расходов")
        verbose_name_plural = _("Категории расходов")

    def __str__(self):
        return self.name

class IncomeCategory(CoreModel):
    """Model representing a category for incomes."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Категория доходов")
        verbose_name_plural = _("Категории доходов")

    def __str__(self):
        return self.name

class Expense(CoreModel):
    """Model representing an expense."""
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, verbose_name=_("Категория"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Сумма"))
    date = models.DateField(verbose_name=_("Дата"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Расход")
        verbose_name_plural = _("Расходы")

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"

class Income(CoreModel):
    """Model representing an income."""
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, verbose_name=_("Категория"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Сумма"))
    date = models.DateField(verbose_name=_("Дата"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Доход")
        verbose_name_plural = _("Доходы")

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"


class RoomProfitability(CoreModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Комната"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Общий доход"))
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Общие расходы"))
    total_service_income = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Общий доход от услуг"))
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Чистая прибыль"))

    class Meta:
        verbose_name = _("Доходность номера")
        verbose_name_plural = _("Доходность номеров")

    def __str__(self):
        return f"Profitability of Room {self.room.room_number} from {self.date_start} to {self.date_end}"

    def save(self, *args, **kwargs):
        # Calculate total income for the room in the specified period
        income_entries = Income.objects.filter(
            room=self.room,
            date__range=[self.date_start, self.date_end]
        )
        self.total_income = sum(entry.amount for entry in income_entries)

        # Calculate total expenses for the room in the specified period
        expense_entries = Expense.objects.filter(
            room=self.room,
            date__range=[self.date_start, self.date_end]
        )
        self.total_expenses = sum(entry.amount for entry in expense_entries)

        # Calculate total service income for the room in the specified period
        service_entries = RoomServiceUsage.objects.filter(
            room=self.room,
            date_used__range=[self.date_start, self.date_end]
        )
        self.total_service_income = sum(entry.price for entry in service_entries)

        # Calculate net profit
        self.net_profit = self.total_income + self.total_service_income - self.total_expenses

        super().save(*args, **kwargs)


class RoomCleaningStatus(CoreModel):
    """Model representing the cleaning status of rooms."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Комната"))
    clean = models.BooleanField(default=False, verbose_name=_("Чистая"))
    last_cleaned = models.DateTimeField(blank=True, null=True, verbose_name=_("Последняя уборка"))

    class Meta:
        verbose_name = _("Статус уборки комнаты")
        verbose_name_plural = _("Статусы уборки комнат")

    def __str__(self):
        return f"{self.room.room_number} - {'Чистая' if self.clean else 'Требует уборки'}"
