from rest_framework import viewsets, status, filters
from rest_framework.response import Response

import django_filters.rest_framework as dfilters

from miniproj.api.hospital.serializers import HospitalSerializer
from miniproj.api.hospital.models import Hospital


class HospitalFilter(dfilters.FilterSet):
    """
    Filterset for Hospital
    """

    name = dfilters.CharFilter(
        field_name="name",
        method="filter_by_name",
        help_text="Filter results by hospital name",
    )
    address = dfilters.CharFilter(
        field_name="address",
        method="filter_by_address",
        help_text="Filter results by hospital address",
    )

    createddt_from = dfilters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        help_text="\
            Filter results by hospital created date FROM \
            (YYYY-MM-DD)",
    )
    createddt_to = dfilters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        help_text="Filter results by hospital created date TO \
            (YYYY-MM-DD)",
    )

    def filter_by_name(self, queryset, name, value):
        """
        Filter Hospital by its name
        """
        return queryset.filter(name__icontains=value)

    def filter_by_address(self, queryset, name, value):
        """
        Filter Hospital by address
        """
        return queryset.filter(address__icontains=value)

    class Meta:
        model = Hospital
        fields = ("name", "address")


class HospitalViewset(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.filter(is_deleted=False).order_by("name")
    filter_backends = [
        dfilters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filter_class = HospitalFilter
    search_fields = ordering_fields = ["id", "name", "address"]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the Hospital."""
        hospital = self.get_object()
        if hospital:
            hospital.is_deleted = True
            hospital.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        hospital_name = request.data["name"]
        if Hospital.objects.filter(name=hospital_name).exists():
            return Response(
                {"detail": "Hospital already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


# @api_view(["GET", "POST"])
# def hospital_list(request, format=None):
#     if request.method == "GET":
#         paginator = pagination.PageNumberPagination()
#         paginator.page_size = 3
#         paginator.page_query_param = "page"
#         qry_set = Hospital.objects.filter(is_deleted=False)
#         order = request.query_params.get("order")
#         if order is not None:
#             qry_set = Hospital.objects.filter(is_deleted=False).order_by(order)
#         hospitals = paginator.paginate_queryset(queryset=qry_set, request=request)
#         serializer = HospitalSerializer(hospitals, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     elif request.method == "POST":
#         serializer = HospitalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT"])
# def hospital_details(request, id, format=None):
#     try:
#         hospital = Hospital.objects.get(id=id)
#     except Hospital.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#         # return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = HospitalSerializer(hospital)
#         # return JsonResponse(serializer.data)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         data = parsers.JSONParser().parse(request)
#         serializer = HospitalSerializer(hospital, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#             # return Response(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["PUT"])
# def hospital_remove(request, id, format=None):
#     try:
#         hospital = Hospital.objects.get(id=id)
#     except Hospital.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "PUT":
#         data = parsers.JSONParser().parse(request)
#         data["is_deleted"] = 1
#         serializer = HospitalSerializer(hospital, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
