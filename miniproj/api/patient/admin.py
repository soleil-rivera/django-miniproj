from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.patient.models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "address", "phone_number")
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_patient"]

    def get_queryset(self, request):
        return Patient.objects.filter(is_deleted=False).order_by("first_name")

    @admin.action(description="Delete selected patient(s)")
    def delete_patient(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d patient was successfully deleted.",
                "%d patients were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Patient, PatientAdmin)
