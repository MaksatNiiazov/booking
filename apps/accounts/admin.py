from django.contrib import admin
from apps.accounts.models import UserAccount, Owner


@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):

    list_display = ("inn", "is_active")
    search_fields = ("inn",)
