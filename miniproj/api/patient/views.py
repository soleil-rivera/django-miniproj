from rest_framework import viewsets, status, filters
from rest_framework.response import Response

import django_filters.rest_framework as dfilters

from miniproj.api.patient.models import Patient
from miniproj.api.patient.serializers import PatientSerializer


class PatientFilter(dfilters.FilterSet):
    """
    Filterset for Patient
    """

    id = dfilters.CharFilter(
        field_name="id",
        method="filter_by_id",
        help_text="Filter results by Patient ID",
    )
    first_name = dfilters.CharFilter(
        field_name="first_name",
        method="filter_by_first_name",
        help_text="Filter results by Patient first_name",
    )
    last_name = dfilters.CharFilter(
        field_name="last_name",
        method="filter_by_last_name",
        help_text="Filter results by Patient last_name",
    )
    middle_name = dfilters.CharFilter(
        field_name="middle_name",
        method="filter_by_middle_name",
        help_text="Filter results by Patient middle_name",
    )
    address = dfilters.CharFilter(
        field_name="address",
        method="filter_by_address",
        help_text="Filter results by Patient address",
    )
    phone_number = dfilters.CharFilter(
        field_name="phone_number",
        method="filter_by_phone_number",
        help_text="Filter results by Patient phone_number",
    )
    createddt_from = dfilters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        help_text="\
            Filter results by Patient created date FROM \
            (YYYY-MM-DD)",
    )
    createddt_to = dfilters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        help_text="Filter results by Patient created date TO \
            (YYYY-MM-DD)",
    )

    def filter_by_id(self, queryset, name, value):
        """
        Filter Patient by its ID
        """
        return queryset.filter(id=value)

    def filter_by_first_name(self, queryset, name, value):
        """
        Filter Patient by first_name
        """
        return queryset.filter(first_name__icontains=value)

    def filter_by_last_name(self, queryset, name, value):
        """
        Filter Patient by last_name
        """
        return queryset.filter(last_name__icontains=value)

    def filter_by_middle_name(self, queryset, name, value):
        """
        Filter Patient by middle_name
        """
        return queryset.filter(middle_name__icontains=value)

    def filter_by_address(self, queryset, name, value):
        """
        Filter Patient by address
        """
        return queryset.filter(address__icontains=value)

    def filter_by_phone_number(self, queryset, name, value):
        """
        Filter Patient by phone_number
        """
        return queryset.filter(phone_number__icontains=value)

    class Meta:
        model = Patient
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "address",
            "phone_number",
        )


class PatientViewset(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.filter(is_deleted=False).order_by("first_name")
    filter_backends = [
        dfilters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PatientFilter
    search_fields = ordering_fields = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "address",
        "phone_number",
    ]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the Patient."""
        patient = self.get_object()
        if patient:
            patient.is_deleted = True
            patient.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
