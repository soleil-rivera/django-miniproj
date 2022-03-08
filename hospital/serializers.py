from rest_framework import serializers
from .models import Hospital


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    # def create(self, validated_data):
    #     return Hospital.objects.create(validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.address = validated_data.get("address", instance.address)
    #     instance.is_deleted = validated_data.get("is_deleted", instance.is_deleted)

    #     instance.save()
    #     return instance

    class Meta:
        model = Hospital
        fields = ("id", "name", "address", "is_deleted", "created", "last_updated")
