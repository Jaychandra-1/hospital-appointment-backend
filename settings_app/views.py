from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SystemSettings
from .serializers import SystemSettingsSerializer


@api_view(["GET","PUT"])
def admin_profile(request):

    settings = SystemSettings.objects.first()

    if settings is None:

        settings = SystemSettings.objects.create(
            admin_name="Admin",
            admin_email="admin@gmail.com",
            admin_phone="9876543210",
            working_hours="09:00 AM - 06:00 PM"
        )

    if request.method == "GET":

        return Response({

            "name": settings.admin_name,

            "email": settings.admin_email,

            "phone": settings.admin_phone

        })

    settings.admin_name = request.data["name"]

    settings.admin_email = request.data["email"]

    settings.admin_phone = request.data["phone"]

    settings.save()

    return Response({"message":"Updated"})
@api_view(["GET","PUT"])
def system_settings(request):

    settings = SystemSettings.objects.first()

    if request.method == "GET":

        serializer = SystemSettingsSerializer(settings)

        return Response(serializer.data)

    serializer = SystemSettingsSerializer(
        settings,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)