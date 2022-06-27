from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.lab_storage.models import LabStorage


class LabStorageAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "get_orders")
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_labstorage"]

    def get_queryset(self, request):
        return LabStorage.objects.filter(is_deleted=False).order_by("name")

    def get_orders(self, obj):
        return "\n".join([p.internal_id for p in obj.orders.all()])

    @admin.action(description="Delete selected lab storage(s)")
    def delete_labstorage(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d lab storage was successfully deleted.",
                "%d lab storages were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(LabStorage, LabStorageAdmin)
