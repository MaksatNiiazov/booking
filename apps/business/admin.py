from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import CompanySector, Document


@admin.register(CompanySector)
class CompanySectorAdmin(admin.ModelAdmin):
    list_display = ["company", "sector", "is_active", "verified"]
    list_filter = ["company", "sector", "is_active"]
    search_fields = ["company__name", "sector__name"]

    def save_model(self, request, obj, form, change):
        if obj.verified and not all(
            doc.verified for doc in Document.objects.filter(company_sector=obj)
        ):
            # Добавление пользовательского сообщения об ошибке
            messages.error(
                request,
                _(
                    "Not all documents are verified for the sector: '%s'. Verification status not changed."
                )
                % obj.sector,
            )
        else:
            super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        """Override to eliminate the default "was changed successfully" message."""
        if "_continue" not in request.POST:
            if messages.get_messages(request):
                return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)

    def response_post_save_change(self, request, obj):
        """Hook to do something after saving an object through the 'Save and continue editing' button."""
        return super().response_post_save_change(request, obj)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "company_sector", "upload_date", "verified"]
    list_filter = ["company_sector", "upload_date"]
    search_fields = [
        "name",
        "company_sector__company__name",
        "company_sector__sector__name",
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "document" in form.base_fields:
            form.base_fields["document"].widget.attrs.update(
                {"accept": "application/pdf, application/vnd.ms-excel"}
            )
        return form
