from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

import django_filters.rest_framework as dfilters
from django.utils.decorators import method_decorator

from miniproj.api.lab_storage.serializers import (
    LabStorageSerializer,
)
from miniproj.api.lab_storage.models import LabStorage

from miniproj.api.order.models import Order
from miniproj.constants import OrderStatus


class LabStorageFilter(dfilters.FilterSet):
    """
    Filterset for Lab Storage
    """

    id = dfilters.CharFilter(
        field_name="id",
        method="filter_by_id",
        help_text="Filter results by Lab Storage ID",
    )
    name = dfilters.CharFilter(
        field_name="name",
        method="filter_by_name",
        help_text="Filter results by Lab Storage name",
    )
    location = dfilters.CharFilter(
        field_name="location",
        method="filter_by_location",
        help_text="Filter results by Lab Storage location",
    )
    orders = dfilters.CharFilter(
        field_name="orders",
        method="filter_by_orders",
        help_text="Filter results by Lab Storage orders internal id",
    )
    createddt_from = dfilters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        help_text="\
            Filter results by Lab Storage created date FROM \
            (YYYY-MM-DD)",
    )
    createddt_to = dfilters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        help_text="Filter results by Lab Storage created date TO \
            (YYYY-MM-DD)",
    )

    def filter_by_id(self, queryset, name, value):
        """
        Filter LabStorage by its ID
        """
        return queryset.filter(id=value)

    def filter_by_name(self, queryset, name, value):
        """
        Filter Lab Storage by its name
        """
        return queryset.filter(name__icontains=value)

    def filter_by_location(self, queryset, name, value):
        """
        Filter Lab Storage by location
        """
        return queryset.filter(location__icontains=value)

    def filter_by_orders(self, queryset, name, value):
        """
        Filter Lab Storage by orders
        """
        return queryset.filter(orders__internal_id__icontains=value)

    class Meta:
        model = LabStorage
        fields = ("name", "location")


order_ids_param = openapi.Parameter(
    "order_ids",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="Order Ids Parameter.",
)


@method_decorator(
    name="add_order",
    decorator=swagger_auto_schema(
        operation_summary="Add order(s) in Laboratory Storage.",
        operation_description="Add order(s) in Laboratory Storage",
        manual_parameters=[order_ids_param],
        responses={
            200: openapi.Response("Order(s) add."),
            404: openapi.Response("Not Found."),
        },
    ),
)
@method_decorator(
    name="remove_order",
    decorator=swagger_auto_schema(
        operation_summary="Remove order(s) in Laboratory Storage.",
        operation_description="Remove order(s) in Laboratory Storage",
        manual_parameters=[order_ids_param],
        responses={
            200: openapi.Response("Order(s) removed."),
            404: openapi.Response("Not Found."),
        },
    ),
)
class LabStorageViewset(viewsets.ModelViewSet):
    serializer_class = LabStorageSerializer
    queryset = LabStorage.objects.filter(is_deleted=False).order_by("name")
    filter_backends = [
        dfilters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = LabStorageFilter
    search_fields = ordering_fields = [
        "id",
        "name",
        "location",
        "orders__internal_id",
    ]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the Laboratory Storage."""
        lab_storage = self.get_object()
        if lab_storage:
            if lab_storage.orders.all():
                return Response(
                    {"detail": "Cannot delete LabStorage. At least 1 Order is stored."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            lab_storage.is_deleted = True
            lab_storage.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        lab_name = request.data["name"]
        if LabStorage.objects.filter(name=lab_name).exists():
            return Response(
                {"detail": "Laboratory Storage name already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def add_order(self, request, pk=None):
        order_ids = self.request.query_params.get("order_ids", None)
        labstorage = self.get_object()

        if not order_ids:
            return Response(
                {"detail": "No IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_ids = order_ids.split(",")
        try:
            orders = Order.objects.filter(id__in=order_ids).all()
            if len(orders) != len(set(order_ids)):
                return Response(
                    {"detail": "Cannot add. At least one order not existing."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception:
            return Response(
                {"detail": "Invalid value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        all_orders = LabStorage.objects.all().values("orders")
        distinct_orders = []
        for order in all_orders:
            if order:
                distinct_orders.append(order["orders"])

        stored_orders = []
        for order in orders:
            get_order = Order.objects.get(id=order.id)
            if get_order.id in distinct_orders:
                stored_orders.append(str(get_order.internal_id))
        if stored_orders:
            stored_orders = ", ".join(stored_orders)
            return Response(
                {"detail": f"Cannot add. Order(s) {stored_orders} already stored."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for order in orders:
            labstorage.orders.add(order.id)
            order.status = OrderStatus.STORED
            order.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def remove_order(self, request, pk=None):
        order_ids = self.request.query_params.get("order_ids", None)
        labstorage = self.get_object()

        if not order_ids:
            return Response(
                {"detail": "No IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_ids = order_ids.split(",")
        try:
            orders = Order.objects.filter(id__in=order_ids).all()
            if len(orders) != len(set(order_ids)):
                return Response(
                    {"detail": "Cannot remove. At least one order not existing."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception:
            return Response(
                {"detail": "Invalid value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stored_orders = []
        for order in orders:
            get_order = Order.objects.get(id=order.id)
            lab_order = labstorage.orders.filter(id=get_order.id)
            if not lab_order:
                stored_orders.append(str(get_order.internal_id))
        if stored_orders:
            stored_orders = ", ".join(stored_orders)
            return Response(
                {
                    "detail": f"Cannot remove. Order(s) {stored_orders} not stored in this LabStorage."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        for order in orders:
            labstorage.orders.remove(order.id)
            order.status = OrderStatus.RECEIVED
            order.save()

        return Response(status=status.HTTP_200_OK)


#    @action(detail=True, methods=["delete"])
#     def remove_order(self, request, pk=None):
#         labstorage = self.get_object()
#         request_orders = request.data["orders"]
#         lab_orders = labstorage.orders.all()

#         if request_orders:
#             for order_id in request_orders:
#                 try:
#                     order = Order.objects.get(id=order_id)
#                     lab_orders = labstorage.orders.filter(id=order_id)
#                     if lab_orders:
#                         labstorage.orders.remove(order.id)
#                         order.status = OrderStatus.RECEIVED
#                         order.save()
#                         return Response(status=status.HTTP_200_OK)
#                     return Response(
#                         {
#                             "detail": "Cannot remove. Order(s) does not exist in this Lab."
#                         },
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#                 except Order.DoesNotExist:
#                     return Response(
#                         {"detail": "Cannot remove. Order(s) does not exist."},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#         return Response(
#             {"detail": "No order(s) provided."}, status=status.HTTP_400_BAD_REQUEST
#         )
