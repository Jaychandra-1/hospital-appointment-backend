from rest_framework import viewsets
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def doctor_login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    doctor = Doctor.objects.filter(
        email=email,
        password=password
    ).first()

    if doctor:

        return Response({
            "success": True,
            "doctor": DoctorSerializer(doctor).data
        })

    return Response({
        "success": False,
        "message": "Invalid Email or Password"
    }, status=401)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from .models import Doctor
from .serializers import DoctorSerializer


@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def doctor_profile(request, pk):

    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "GET":
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    serializer = DoctorSerializer(
        doctor,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)