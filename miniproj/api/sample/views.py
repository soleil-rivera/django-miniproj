from rest_framework import viewsets, status, filters
from rest_framework.response import Response

import django_filters.rest_framework as dfilters

from miniproj.api.sample.models import Sample
from miniproj.api.sample.serializers import SampleSerializer


class SampleFilter(dfilters.FilterSet):
    """
    Filterset for Sample
    """

    id = dfilters.CharFilter(
        field_name="id",
        method="filter_by_id",
        help_text="Filter results by Sample ID",
    )
    sample_id = dfilters.CharFilter(
        field_name="sample_id",
        method="filter_by_sample_id",
        help_text="Filter results by Sample sample_id",
    )
    first_name = dfilters.CharFilter(
        field_name="first_name",
        method="filter_by_first_name",
        help_text="Filter results by Sample first_name",
    )
    createddt_from = dfilters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        help_text="\
            Filter results by Sample created date FROM \
            (YYYY-MM-DD)",
    )
    createddt_to = dfilters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        help_text="Filter results by Sample created date TO \
            (YYYY-MM-DD)",
    )

    def filter_by_id(self, queryset, name, value):
        """
        Filter Sample by its ID
        """
        return queryset.filter(id=value)

    def filter_by_sample_id(self, queryset, name, value):
        """
        Filter Sample by its sample_id
        """
        return queryset.filter(sample_id__icontains=value)

    def filter_by_first_name(self, queryset, name, value):
        """
        Filter Sample by first_name
        """
        return queryset.filter(first_name__first_name__icontains=value)

    class Meta:
        model = Sample
        fields = ("sample_id", "first_name")


class SampleViewset(viewsets.ModelViewSet):
    serializer_class = SampleSerializer
    queryset = Sample.objects.filter(is_deleted=False).order_by("sample_id")
    filter_backends = [
        dfilters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SampleFilter
    search_fields = ordering_fields = ["id", "sample_id", "first_name__first_name"]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the Sample."""
        sample = self.get_object()
        if sample:
            sample.is_deleted = True
            sample.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        sid = request.data["sample_id"]
        if Sample.objects.filter(sample_id=sid).exists():
            return Response(
                {"detail": "Sample ID already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)
