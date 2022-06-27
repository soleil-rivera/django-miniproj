from rest_framework import viewsets, status, filters
from rest_framework.response import Response

import django_filters.rest_framework as dfilters

from miniproj.api.order.models import Order
from miniproj.api.order.serializers import OrderSerializer


class OrderFilter(dfilters.FilterSet):
    """
    Filterset for Order
    """

    internal_id = dfilters.CharFilter(
        field_name="internal_id",
        method="filter_by_internal_id",
        help_text="Filter results by Order internal_id",
    )
    status = dfilters.CharFilter(
        field_name="status",
        method="filter_by_status",
        help_text="Filter results by Order status",
    )
    sample = dfilters.CharFilter(
        field_name="sample",
        method="filter_by_sample",
        help_text="Filter results by Order sample",
    )
    hospital = dfilters.CharFilter(
        field_name="hospital",
        method="filter_by_hospital",
        help_text="Filter results by Order hospital",
    )
    physician = dfilters.CharFilter(
        field_name="physician",
        method="filter_by_physician",
        help_text="Filter results by Order physician",
    )
    createddt_from = dfilters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        help_text="\
            Filter results by Order created date FROM \
            (YYYY-MM-DD)",
    )
    createddt_to = dfilters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        help_text="Filter results by Order created date TO \
            (YYYY-MM-DD)",
    )
    sampletaken_createddt_from = dfilters.DateFilter(
        field_name="date_sample_taken",
        lookup_expr="gte",
        help_text="\
            Filter results by Order created date FROM \
            (YYYY-MM-DD)",
    )
    sampletaken_createddt_to = dfilters.DateFilter(
        field_name="date_sample_taken",
        lookup_expr="lte",
        help_text="Filter results by Order created date TO \
            (YYYY-MM-DD)",
    )

    def filter_by_internal_id(self, queryset, name, value):
        """
        Filter Order by internal_id
        """
        return queryset.filter(internal_id__icontains=value)

    def filter_by_status(self, queryset, name, value):
        """
        Filter Order by status
        """
        return queryset.filter(status__icontains=value)

    def filter_by_sample(self, queryset, name, value):
        """
        Filter Order by sample
        """
        return queryset.filter(sample__sample_id__icontains=value)

    def filter_by_hospital(self, queryset, name, value):
        """
        Filter Order by hospital
        """
        return queryset.filter(hospital__name__icontains=value)

    def filter_by_physician(self, queryset, name, value):
        """
        Filter Order by physician
        """
        return queryset.filter(physician__first_name__icontains=value)

    class Meta:
        model = Order
        fields = ("internal_id", "status", "sample", "hospital", "physician")


class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_deleted=False).order_by("internal_id")
    filter_backends = [
        dfilters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filter_class = OrderFilter
    search_fields = ordering_fields = [
        "id",
        "internal_id",
        "date_sample_taken",
        "sample__sample_id",
        "status",
        "hospital__name",
        "physician__first_name",
    ]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the Order."""
        order = self.get_object()
        if order:
            order.is_deleted = True
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        iid = request.data["internal_id"]
        if Order.objects.filter(internal_id=iid).exists():
            return Response(
                {"detail": "Internal ID already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)
