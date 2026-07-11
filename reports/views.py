from rest_framework.decorators import api_view
from rest_framework.response import Response

from appointments.models import Appointment
from notifications.models import Notification

from .models import MedicalReport
from .serializers import MedicalReportSerializer

@api_view(["POST"])
def create_report(request):

    appointment = Appointment.objects.get(
        id=request.data["appointment_id"]
    )

    report, created = MedicalReport.objects.update_or_create(
        appointment=appointment,
        defaults={
            "diagnosis": request.data["diagnosis"],
            "prescription": request.data["prescription"],
            "advice": request.data["advice"],
        }
    )

    if created:
        Notification.objects.create(
            patient=appointment.patient.name,
            title="Medical Report Ready",
            message=f"Dr. {appointment.doctor.name} has uploaded your medical report.",
            notification_type="Report"
        )

    serializer = MedicalReportSerializer(report)

    return Response(serializer.data)
from accounts.models import Patient

@api_view(["GET"])
def patient_reports(request, patient_name):

    patient = Patient.objects.filter(name=patient_name).first()

    if patient is None:
        return Response({"error": "Patient not found"}, status=404)

    reports = MedicalReport.objects.filter(
        appointment__patient=patient
    )

    serializer = MedicalReportSerializer(reports, many=True)

    return Response(serializer.data)
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def report_detail(request, report_id):

    report = get_object_or_404(
        MedicalReport,
        id=report_id
    )

    serializer = MedicalReportSerializer(report)

    return Response(serializer.data)
@api_view(["PUT"])
def update_report(request, report_id):

    report = get_object_or_404(
        MedicalReport,
        id=report_id
    )

    report.diagnosis = request.data["diagnosis"]
    report.prescription = request.data["prescription"]
    report.advice = request.data["advice"]

    report.save()

    serializer = MedicalReportSerializer(report)

    return Response(serializer.data)