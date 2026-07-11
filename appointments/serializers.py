from rest_framework import serializers
from .models import Appointment
from reports.models import MedicalReport


class AppointmentSerializer(serializers.ModelSerializer):

    doctor = serializers.CharField(source="doctor.name", read_only=True)
    patient = serializers.CharField(source="patient.name", read_only=True)
    specialization = serializers.CharField(
    source="doctor.specialization",
    read_only=True
)

    report_id = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
             "specialization",
            "appointment_date",
            "appointment_time",
            "problem",
            "status",
            "report_id",
        ]

    def get_report_id(self, obj):

        report = MedicalReport.objects.filter(
            appointment=obj
        ).first()

        return report.id if report else None