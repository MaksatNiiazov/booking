from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import CoreModel

User = get_user_model()


class Address(CoreModel):
    line1 = models.CharField(
        max_length=255,
        verbose_name=_("Адресная строка 1"),
        help_text=_("Адрес, почтовый ящик, название компании"),
    )
    line2 = models.CharField(
        max_length=255,
        verbose_name=_("Адресная строка 2"),
        blank=True,
        null=True,
        help_text=_("Квартира, офис, подразделение, здание, этаж и т.д."),
    )
    city = models.CharField(max_length=100, verbose_name=_("Город"))
    state_province = models.CharField(
        max_length=100, verbose_name=_("Штат/Провинция"), blank=True, null=True
    )
    postal_code = models.CharField(max_length=20, verbose_name=_("Почтовый индекс"))
    country = models.CharField(max_length=100, verbose_name=_("Страна"))

    class Meta:
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адреса")

    def __str__(self):
        return f'{self.country} {self.city} {self.line1} {self.line2}'


class Amenity(CoreModel):
    icon = models.FileField(
        upload_to="amenity_icons", blank=True, null=True, verbose_name=_("Иконка")
    )
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Удобство")
        verbose_name_plural = _("Удобства")


class Property(CoreModel):
    TYPE_CHOICES = (
        ("house", _("Дом")),
        ("apartment", _("Квартира")),
        ("hotel", _("Отель")),
    )
    property_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name=_("Тип недвижимости")
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name=_("Адрес")
    )
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name=_("Удобства"))
    available = models.BooleanField(default=True, verbose_name=_("Доступно"))
    procent = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.0, blank=True
    )
    star_rating = models.IntegerField(verbose_name=_("Рейтинг звёзд"))
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    rooms = models.IntegerField(
        help_text=_("Количество доступных комнат"), verbose_name=_("Комнаты")
    )
    verified = models.BooleanField(default=False, verbose_name=_("Проверено"))
    brand = models.CharField(max_length=100, verbose_name=_("Бренд"), blank=True, null=True)

    class Meta:
        verbose_name = _("Недвижимость")
        verbose_name_plural = _("Недвижимость")


class PropertyPhoto(CoreModel):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name=_("Недвижимость")
    )
    photo = models.ImageField(upload_to="property_photos", verbose_name=_("Фото"))

    class Meta:
        verbose_name = _("Фотография недвижимости")
        verbose_name_plural = _("Фотографии недвижимости")


class RoomAmenity(CoreModel):
    icon = models.FileField(
        upload_to="amenity_icons", blank=True, null=True, verbose_name=_("Иконка")
    )
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Удобство комнаты")
        verbose_name_plural = _("Удобства комнат")

    def __str__(self):
        return self.name

class Room(CoreModel):
    hotel = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="hotel_rooms",
        verbose_name=_("Отель"),
    )
    room_number = models.CharField(max_length=20, verbose_name=_("Номер комнаты"))
    room_type = models.CharField(max_length=20, verbose_name=_("Тип комнаты"))
    default_price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Стандартная цена за ночь")
    )
    amenities = models.ManyToManyField(
        RoomAmenity, blank=True, verbose_name=_("Удобства")
    )
    available = models.BooleanField(default=True, verbose_name=_("Доступна"))
    max_adults = models.IntegerField(verbose_name=_('Максимум взрослых'))
    max_children = models.IntegerField(verbose_name=_('Максимум детей'))

    class Meta:
        verbose_name = _("Комната")
        verbose_name_plural = _("Комнаты")


class RoomPhotos(CoreModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Комната"))
    photo = models.ImageField(upload_to="room_photos", verbose_name=_("Фото"))


class Price(CoreModel):
    rooms = models.ManyToManyField(Room, related_name='special_prices', verbose_name=_("Комнаты"))
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена за ночь"))


class Review(models.Model):
    property = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Недвижимость"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Пользователь"),
    )
    comment = models.TextField(
        blank=True,
        null=True,
        help_text="Comment about the property",
        verbose_name=_("Коммент"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.property.name}"
