from rest_framework import serializers
from miniproj.api.lab_storage.models import LabStorage
from miniproj.api.order.models import Order
from miniproj.api.order.serializers import OrderSerializer

from miniproj.constants import Validators


class LabStorageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["orders"] = [g.id for g in instance.orders.filter(is_deleted=False)]
        return rep

    class Meta:
        model = LabStorage
        fields = ("id", "name", "location", "orders")
