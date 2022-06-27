from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.hospital.models import Hospital

admin.site.disable_action("delete_selected")


class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_hospital"]

    def get_queryset(self, request):
        return Hospital.objects.filter(is_deleted=False).order_by("name")

    @admin.action(description="Delete selected hospital(s)")
    def delete_hospital(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d hospital was successfully deleted.",
                "%d hospitals were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Hospital, HospitalAdmin)
