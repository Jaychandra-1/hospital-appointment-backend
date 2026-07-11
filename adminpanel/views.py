from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


@api_view(["GET"])
def dashboard(request):

    today = date.today()

    data = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "today_appointments": Appointment.objects.filter(
            appointment_date=today
        ).count(),
        "pending": Appointment.objects.filter(
            status="Pending"
        ).count(),
        "accepted": Appointment.objects.filter(
            status="Accepted"
        ).count(),
        "completed": Appointment.objects.filter(
            status="Completed"
        ).count(),
        "cancelled": Appointment.objects.filter(
            status="Cancelled"
        ).count(),
    }

    return Response(data)
from appointments.serializers import AppointmentSerializer

@api_view(["GET"])
def recent_appointments(request):

    appointments = Appointment.objects.all().order_by("-id")[:5]

    serializer = AppointmentSerializer(
        appointments,
        many=True
    )

    return Response(serializer.data)
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer


@api_view(["GET"])
def all_appointments(request):

    appointments = Appointment.objects.all().order_by("-id")

    serializer = AppointmentSerializer(
        appointments,
        many=True
    )

    return Response(serializer.data)
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer


@api_view(["GET"])
def all_doctors(request):

    doctors = Doctor.objects.all().order_by("-id")

    serializer = DoctorSerializer(
        doctors,
        many=True
    )

    return Response(serializer.data)