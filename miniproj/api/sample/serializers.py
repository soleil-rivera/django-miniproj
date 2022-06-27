from rest_framework import serializers
from miniproj.api.sample.models import Sample

from miniproj.constants import Validators
from miniproj.api.patient.models import Patient


class SampleSerializer(serializers.ModelSerializer):

    sample_id = serializers.CharField(
        max_length=255,
        required=True,
        validators=[Validators.alpha_num_wsc],
    )
    first_name = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.filter(is_deleted=False)
    )

    def validate_sample_id(self, value):
        if value and Sample.objects.filter(sample_id=value).exists():
            raise serializers.ValidationError("Sample ID already exists.")
        return value

    class Meta:
        model = Sample
        fields = ("id", "sample_id", "first_name")
