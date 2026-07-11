from rest_framework import serializers
from .models import MedicalReport


class MedicalReportSerializer(serializers.ModelSerializer):

    patient = serializers.CharField(
        source="appointment.patient.name",
        read_only=True
    )

    age = serializers.IntegerField(
        source="appointment.patient.age",
        read_only=True
    )

    gender = serializers.CharField(
        source="appointment.patient.gender",
        read_only=True
    )

    phone = serializers.CharField(
        source="appointment.patient.phone",
        read_only=True
    )

    address = serializers.CharField(
        source="appointment.patient.address",
        read_only=True
    )

    doctor = serializers.CharField(
        source="appointment.doctor.name",
        read_only=True
    )

    class Meta:
        model = MedicalReport
        fields = "__all__"