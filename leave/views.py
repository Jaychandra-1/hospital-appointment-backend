from rest_framework.decorators import api_view
from rest_framework.response import Response

from doctors.models import Doctor
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer


@api_view(["POST"])
def create_leave(request):

    doctor = Doctor.objects.get(
        id=request.data["doctor_id"]
    )

    leave = LeaveRequest.objects.create(
        doctor=doctor,
        leave_type=request.data["leave_type"],
        start_date=request.data["start_date"],
        end_date=request.data["end_date"],
        reason=request.data["reason"],
        emergency=request.data.get("emergency", False),
        status="Pending"
    )

    serializer = LeaveRequestSerializer(leave)

    return Response(serializer.data)


@api_view(["GET"])
def doctor_leaves(request, doctor_id):

    leaves = LeaveRequest.objects.filter(
        doctor_id=doctor_id
    )

    serializer = LeaveRequestSerializer(
        leaves,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET"])
def all_leave_requests(request):

    leaves = LeaveRequest.objects.all().order_by("-created_at")

    serializer = LeaveRequestSerializer(
        leaves,
        many=True
    )

    return Response(serializer.data)
from django.shortcuts import get_object_or_404


@api_view(["PUT"])
def approve_leave(request, leave_id):

    leave = get_object_or_404(
        LeaveRequest,
        id=leave_id
    )

    leave.status = "Approved"

    leave.save()

    serializer = LeaveRequestSerializer(leave)

    return Response(serializer.data)


@api_view(["PUT"])
def reject_leave(request, leave_id):

    leave = get_object_or_404(
        LeaveRequest,
        id=leave_id
    )

    leave.status = "Rejected"

    leave.save()

    serializer = LeaveRequestSerializer(leave)

    return Response(serializer.data)