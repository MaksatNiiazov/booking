from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.common.models import CoreModel
from apps.property.models import Room

User = get_user_model()


class Record(CoreModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("Пользователь"),
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name=_("Комната"),
    )
    start_date = models.DateField(verbose_name=_("Дата начала"))
    end_date = models.DateField(verbose_name=_("Дата окончания"))
    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", _("Ожидает")),
            ("confirmed", _("Подтвержден")),
            ("canceled", _("Отменен")),
        ),
        default="pending",
        verbose_name=_("Статус"),
    )
    procent = models.DecimalField(
        max_digits=10,
        blank=True,
        default=0.0,
        decimal_places=10,
        verbose_name=_("Процент"),
    )
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Общая стоимость")
    )

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(
                {
                    "start_date": "Start date must be before end date.",
                    "end_date": "End date must be after start date.",
                }
            )
        overlapping_records = Record.objects.filter(
            room=self.room,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
            status="confirmed",
        ).exclude(uuid=self.uuid)
        if overlapping_records.exists():
            raise ValidationError(
                "There is already a booking for the specified period for this room."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.email}"

