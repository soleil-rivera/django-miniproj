from django.contrib import admin, messages
from django.utils.translation import ngettext

from miniproj.api.sample.models import Sample


class SampleAdmin(admin.ModelAdmin):
    list_display = ("sample_id", "first_name")
    list_per_page = 15
    exclude = ["is_deleted"]
    actions = ["delete_sample"]

    def get_queryset(self, request):
        return Sample.objects.filter(is_deleted=False).order_by("sample_id")

    @admin.action(description="Delete selected sample(s)")
    def delete_sample(self, request, queryset):
        if request.POST:
            self.delete_queryset(request, queryset)
        return super().delete_queryset(request, queryset)

    def delete_queryset(self, request, queryset):
        updated = queryset.update(is_deleted=1)
        self.message_user(
            request,
            ngettext(
                "%d sample was successfully deleted.",
                "%d samples were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Sample, SampleAdmin)
