from django.contrib import admin
import nested_admin
from .models import (
    Address,
    Amenity,
    Property,
    PropertyPhoto,
    Room,
    RoomAmenity,
    RoomPhotos,
    Price,
)


class PropertyPhotoInline(nested_admin.NestedTabularInline):
    model = PropertyPhoto
    extra = 0
    fields = ["photo"]


class RoomPhotosInline(nested_admin.NestedTabularInline):
    model = RoomPhotos
    extra = 0
    fields = ["photo"]


# class RoomAmenityInline(nested_admin.NestedTabularInline):
#     model = Room.amenities.through
#     extra = 0
#     verbose_name = "Room Amenity"
#     verbose_name_plural = "Room Amenities"


class RoomInline(nested_admin.NestedTabularInline):
    model = Room
    inlines = [RoomPhotosInline]
    extra = 0
    fields = ["room_number", "room_type", "default_price_per_night", "available", 'max_adults', 'max_children', 'amenities']


@admin.register(Property)
class PropertyAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        "name",
        "property_type",
        "address",
        "available",
        "star_rating",
        "rooms",
        "verified",
    ]
    search_fields = [
        "name",
        "description",
    ]
    list_filter = [
        "available",
        "property_type",
        "verified",
    ]
    inlines = [PropertyPhotoInline, RoomInline]
    filter_horizontal = ["amenities"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "property_type",
                    "star_rating",
                    "rooms",
                    "verified",
                    "available",
                    "procent",
                )
            },
        ),
        ("Address", {"fields": ("address",)}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "line1",
        "line2",
        "city",
        "state_province",
        "postal_code",
        "country",
    ]
    search_fields = ["line1", "city", "postal_code", "country"]
    list_filter = ["country", "state_province"]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass