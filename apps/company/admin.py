from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Company, Worker
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


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role']
    list_filter = ['company', 'role']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    autocomplete_fields = ['user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            kwargs['queryset'] = Group.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
