from rest_framework import serializers
from miniproj.api.hospital.models import Hospital

from miniproj.constants import Validators


class HospitalSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, max_length=255, validators=[Validators.alpha_only]
    )
    address = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = Hospital
        fields = ("id", "name", "address")
