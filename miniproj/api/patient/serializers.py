from rest_framework import serializers
from miniproj.api.patient.models import Patient

from miniproj.constants import Validators


class PatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True, max_length=255, validators=[Validators.alpha_only]
    )
    middle_name = serializers.CharField(
        required=True, max_length=255, validators=[Validators.alpha_only]
    )
    last_name = serializers.CharField(
        required=True, max_length=255, validators=[Validators.alpha_only]
    )
    address = serializers.CharField(required=True, max_length=255)
    phone_number = serializers.CharField(
        max_length=20, validators=[Validators.num_only]
    )

    class Meta:
        model = Patient
        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "address",
            "phone_number",
        )
