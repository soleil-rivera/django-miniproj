from email.policy import default
from rest_framework import serializers
from miniproj.api.order.models import Order
from miniproj.api.sample.models import Sample
from miniproj.api.hospital.models import Hospital
from miniproj.api.physician.models import Physician

from miniproj.constants import OrderStatus, Validators


class OrderSerializer(serializers.ModelSerializer):
    internal_id = serializers.CharField(
        required=True, max_length=255, validators=[Validators.alpha_num_wsc]
    )
    date_sample_taken = serializers.DateField(required=True)
    sample = serializers.PrimaryKeyRelatedField(
        queryset=Sample.objects.filter(is_deleted=False), required=False
    )
    status = serializers.CharField(
        max_length=20, read_only=True, default=OrderStatus.RECEIVED
    )
    hospital = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.filter(is_deleted=False), required=False
    )
    physician = serializers.PrimaryKeyRelatedField(
        queryset=Physician.objects.filter(is_deleted=False), required=False
    )

    # def validate_internal_id(self, value):
    #     if value and Order.objects.filter(internal_id=value).exists():
    #         raise serializers.ValidationError("Internal ID already exists.")
    #     return value

    class Meta:
        model = Order
        fields = (
            "id",
            "internal_id",
            "date_sample_taken",
            "sample",
            "status",
            "hospital",
            "physician",
        )
