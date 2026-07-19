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
from rest_framework.decorators import api_view
from rest_framework.response import Response

SYSTEM_SETTINGS = {
    "appointment_duration": 30,
    "consultation_fee": 500,
    "working_hours": "09:00-18:00",
    "emergency_contact": "+91 9876543210"
}

ADMIN_PROFILE = {
    "name": "Administrator",
    "email": "admin@medicare.com",
    "phone": "9876543210"
}


@api_view(["GET", "PUT"])
def admin_profile(request):

    global ADMIN_PROFILE

    if request.method == "GET":
        return Response(ADMIN_PROFILE)

    ADMIN_PROFILE["name"] = request.data.get(
        "name",
        ADMIN_PROFILE["name"]
    )

    ADMIN_PROFILE["email"] = request.data.get(
        "email",
        ADMIN_PROFILE["email"]
    )

    ADMIN_PROFILE["phone"] = request.data.get(
        "phone",
        ADMIN_PROFILE["phone"]
    )

    return Response({
        "message": "Profile Updated Successfully",
        "profile": ADMIN_PROFILE
    })

@api_view(["GET", "PUT"])
def system_settings(request):

    global SYSTEM_SETTINGS

    if request.method == "PUT":
        SYSTEM_SETTINGS = request.data

    return Response(SYSTEM_SETTINGS)
@api_view(["GET", "PUT"])
def settings(request):

    global SYSTEM_SETTINGS

    if request.method == "GET":
        return Response(SYSTEM_SETTINGS)

    SYSTEM_SETTINGS["appointment_duration"] = request.data.get(
        "appointment_duration",
        SYSTEM_SETTINGS["appointment_duration"]
    )

    SYSTEM_SETTINGS["consultation_fee"] = request.data.get(
        "consultation_fee",
        SYSTEM_SETTINGS["consultation_fee"]
    )

    SYSTEM_SETTINGS["working_hours"] = request.data.get(
        "working_hours",
        SYSTEM_SETTINGS["working_hours"]
    )

    SYSTEM_SETTINGS["emergency_contact"] = request.data.get(
        "emergency_contact",
        SYSTEM_SETTINGS["emergency_contact"]
    )

    return Response({
        "message": "System settings updated successfully",
        "settings": SYSTEM_SETTINGS
    })