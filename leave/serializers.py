from rest_framework import serializers
from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(
        source="doctor.name",
        read_only=True
    )

    class Meta:
        model = LeaveRequest
        fields = "__all__"