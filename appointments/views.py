import razorpay

from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer

from accounts.models import Patient
from doctors.models import Doctor

from notifications.models import Notification
from leave.models import LeaveRequest
@api_view(["GET"])
def patient_appointments(request, patient_name):

    patients = Patient.objects.filter(name=patient_name)

    appointments = Appointment.objects.filter(
    patient__in=patients
).order_by("-appointment_date", "-appointment_time")

    serializer = AppointmentSerializer(
        appointments,
        many=True
    )

    return Response(serializer.data)
@api_view(["GET"])
def doctor_appointments(request, doctor_name):

    print("Received doctor:", doctor_name)

    doctor = Doctor.objects.filter(name=doctor_name).first()

    print("Doctor Found:", doctor)

    appointments = Appointment.objects.filter(
        doctor=doctor
    )

    print("Appointments Count:", appointments.count())
    for appointment in appointments:
        print(
        "Appointment:",
        appointment.id,
        appointment.patient.name,
        appointment.doctor.name,
        appointment.status
    )
    serializer = AppointmentSerializer(
        appointments,
        many=True
    )

    return Response(serializer.data)
@api_view(["GET", "PUT"])
def update_appointment_status(request, appointment_id):

    try:
        appointment = Appointment.objects.get(id=appointment_id)

        # GET: Show appointment details
        if request.method == "GET":
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)

        # PUT: Update appointment status
        status = request.data.get("status")

        if not status:
            return Response(
                {"error": "Status is required"},
                status=400
            )

        # Save new status
        appointment.status = status
        appointment.save()

        # Create notification if appointment is cancelled
        if status == "Cancelled":

            Notification.objects.create(
                patient=appointment.patient.name,
                title="Appointment Cancelled",
                message=f"Your appointment with {appointment.doctor.name} has been cancelled successfully.",
                notification_type="Appointment"
            )

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)

    except Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found"},
            status=404
        )
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


@api_view(["POST"])
def create_order(request):

    amount = int(request.data.get("amount")) * 100

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return Response({
        "order_id": payment["id"],
        "amount": payment["amount"],
        "key": settings.RAZORPAY_KEY_ID
    })


@api_view(["POST"])
def create_appointment(request):

    print("========== REQUEST ==========")
    print(request.data)

    try:

        patient_name = request.data.get("patient_name")
        doctor_name = request.data.get("doctor")
        
        print("Received patient_name =", repr(patient_name))
        print("Received doctor_name =", repr(doctor_name))
        

        print("Patient:", patient_name)
        print("Doctor:", doctor_name)

        patient = Patient.objects.filter(name=patient_name).first()
        doctor = Doctor.objects.filter(name=doctor_name).first()

        print("Patient Found:", patient)
        print("Doctor Found:", doctor)

        appointment_date = request.data.get("appointment_date")

        leave_exists = LeaveRequest.objects.filter(
            doctor=doctor,
            status="Approved",
            start_date__lte=appointment_date,
            end_date__gte=appointment_date
            ).exists()
        
        if leave_exists:

            return Response(
                {
                    "error": "Doctor is on approved leave on this date."
                    },
                    status=400
                    )
        if patient is None:
            return Response({"error": "Patient not found"}, status=400)
        if doctor is None:
            return Response({"error": "Doctor not found"}, status=400)


        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=request.data.get("appointment_date"),
            appointment_time=request.data.get("appointment_time"),
            problem=request.data.get("symptoms"),
            status="Pending"
        )
        print("Appointment ID:", appointment.id)
        print("Saved Patient:", appointment.patient.name)
        print("Saved Doctor:", appointment.doctor.name)
        
        Notification.objects.create(
    patient=patient.name,
    title="Appointment Booked",
    message=f"Your appointment with {doctor.name} has been booked successfully.",
    notification_type="Appointment"
)
        Notification.objects.create(
    patient=patient.name,
    title="Payment Successful",
    message="Your payment has been received successfully.",
    notification_type="Payment"
)

        print("Appointment Saved Successfully!")

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()

        return Response(
            {"error": str(e)},
            status=400
        )
@api_view(["GET"])
def appointment_history(request, patient_name):

    patients = Patient.objects.filter(name=patient_name)

    appointments = Appointment.objects.filter(
        patient__in=patients
    ).order_by("-appointment_date", "-appointment_time")

    serializer = AppointmentSerializer(
        appointments,
        many=True
    )

    return Response(serializer.data)
@api_view(["GET"])
def track_appointment(request, appointment_id):

    try:

        appointment = Appointment.objects.get(id=appointment_id)

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)

    except Appointment.DoesNotExist:

        return Response(
            {"error": "Appointment not found"},
            status=404
        )

from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

from django.utils.timezone import now


@api_view(["GET"])
def admin_dashboard(request):

    total_patients = Patient.objects.count()

    total_doctors = Doctor.objects.count()

    total_appointments = Appointment.objects.count()

    today_appointments = Appointment.objects.filter(
        appointment_date=now().date()
    ).count()

    return Response({
        "patients": total_patients,
        "doctors": total_doctors,
        "appointments": total_appointments,
        "todayAppointments": today_appointments
    })
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def appointments_chart(request):

    filter_type = request.GET.get("filter", "week")

    if filter_type == "month":
        start_date = now().date() - timedelta(days=30)
    else:
        start_date = now().date() - timedelta(days=7)

    appointments = (
        Appointment.objects
        .filter(appointment_date__gte=start_date)
        .values("appointment_date")
        .annotate(total=Count("id"))
        .order_by("appointment_date")
    )

    labels = []
    values = []

    for item in appointments:
        labels.append(item["appointment_date"].strftime("%d %b"))
        values.append(item["total"])

    return Response({
        "labels": labels,
        "values": values
    })
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Appointment


@api_view(["GET"])
def appointment_status_chart(request):

    pending = Appointment.objects.filter(status="Pending").count()

    confirmed = Appointment.objects.filter(status="Confirmed").count()

    completed = Appointment.objects.filter(status="Completed").count()

    cancelled = Appointment.objects.filter(status="Cancelled").count()

    return Response({

        "labels": [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ],

        "values": [
            pending,
            confirmed,
            completed,
            cancelled
        ]

    })