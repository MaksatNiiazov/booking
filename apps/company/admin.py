from django.contrib import admin
from .models import Company
from django.utils.translation import gettext_lazy as _


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "industry",
        "phone",
        "email",
        "website",
        "established_date",
    )
    list_filter = ("industry", "established_date")
    search_fields = (
        "name",
        "owner__username",
        "industry",
        "address",
        "phone",
        "email",
        "website",
    )
    date_hierarchy = "established_date"
    ordering = ("name", "industry")

    fieldsets = (
        (None, {"fields": ("name", "owner", "industry", "established_date")}),
        (
            _("Contact Information"),
            {
                "classes": ("collapse",),
                "fields": ("address", "phone", "email", "website"),
            },
        ),
    )
