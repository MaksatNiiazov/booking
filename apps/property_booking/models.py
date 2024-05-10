from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.property.models import Room
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
