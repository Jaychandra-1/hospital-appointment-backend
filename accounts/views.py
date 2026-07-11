from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Patient, PasswordResetOTP
from .serializers import PatientSerializer

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils import timezone

from datetime import timedelta
import random


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


@api_view(["POST"])
def patient_login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    try:
        patient = Patient.objects.get(email=email)

        if check_password(password, patient.password):
            return Response({
                "success": True,
                "id": patient.id,
                "name": patient.name,
                "email": patient.email,
                "age": patient.age,
                "gender": patient.gender
            })

        return Response({
            "success": False,
            "message": "Invalid Email or Password"
        }, status=401)

    except Patient.DoesNotExist:
        return Response({
            "success": False,
            "message": "Invalid Email or Password"
        }, status=401)


@api_view(["POST"])
def forgot_password(request):

    email = request.data.get("email")

    try:
        Patient.objects.get(email=email)

    except Patient.DoesNotExist:
        return Response(
            {
                "error": "No account found with this email."
            },
            status=404,
        )

    otp = str(random.randint(100000, 999999))

    # Delete old OTP
    PasswordResetOTP.objects.filter(email=email).delete()

    # Save new OTP
    PasswordResetOTP.objects.create(
        email=email,
        otp=otp,
    )

    # Debug
    print("===================================")
    print("Email:", email)
    print("Generated OTP:", otp)
    print("===================================")

    # Send Email
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP is {otp}. It is valid for 5 minutes.",
        from_email="cjaya8555@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

    print("OTP email sent successfully")

    return Response(
        {
            "message": "OTP sent successfully."
        }
    )


@api_view(["POST"])
def verify_otp(request):

    email = request.data.get("email")
    otp = request.data.get("otp")

    try:
        otp_obj = PasswordResetOTP.objects.get(
            email=email,
            otp=otp
        )

    except PasswordResetOTP.DoesNotExist:
        return Response(
            {
                "error": "Invalid OTP"
            },
            status=400
        )

    if timezone.now() > otp_obj.created_at + timedelta(minutes=5):

        otp_obj.delete()

        return Response(
            {
                "error": "OTP Expired"
            },
            status=400
        )

    otp_obj.verified = True
    otp_obj.save()

    return Response(
        {
            "message": "OTP Verified"
        }
    )


@api_view(["POST"])
def reset_password(request):

    email = request.data.get("email")
    password = request.data.get("new_password")

    try:
        otp_obj = PasswordResetOTP.objects.get(
            email=email,
            verified=True
        )

    except PasswordResetOTP.DoesNotExist:
        return Response(
            {
                "error": "OTP verification required"
            },
            status=400
        )

    patient = Patient.objects.get(email=email)

    patient.password = make_password(password)
    patient.save()

    otp_obj.delete()

    return Response(
        {
            "message": "Password Updated Successfully"
        }
    )
from appointments.models import Appointment
from reports.models import MedicalReport
from notifications.models import Notification
from reviews.models import Review


@api_view(["GET"])
def dashboard_counts(request, patient_name):

    appointments = Appointment.objects.filter(
        patient__name=patient_name
    ).count()

    reports = MedicalReport.objects.filter(
        appointment__patient__name=patient_name
    ).count()

    notifications = Notification.objects.filter(
        patient=patient_name
    ).count()

    reviews = Review.objects.filter(
        patient=patient_name
    ).count()

    return Response({
        "appointments": appointments,
        "reports": reports,
        "notifications": notifications,
        "reviews": reviews
    })