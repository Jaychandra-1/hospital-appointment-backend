from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return Patient.objects.create(**validated_data)