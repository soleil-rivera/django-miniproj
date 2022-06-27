from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.physician.models import Physician


class PhysicianAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "address", "phone_number")
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_physician"]

    def get_queryset(self, request):
        return Physician.objects.filter(is_deleted=False).order_by("first_name")

    @admin.action(description="Delete selected physician(s)")
    def delete_physician(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d physician was successfully deleted.",
                "%d physicians were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Physician, PhysicianAdmin)
