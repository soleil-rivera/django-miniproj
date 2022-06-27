from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "internal_id",
        "date_sample_taken",
        "sample",
        "status",
        "hospital",
        "physician",
    )
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_order"]
    readonly_fields = ("status",)

    def get_queryset(self, request):
        return Order.objects.filter(is_deleted=False).order_by("internal_id")

    @admin.action(description="Delete selected Order(s)")
    def delete_order(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d Order was successfully deleted.",
                "%d Order were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Order, OrderAdmin)
