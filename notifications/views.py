from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@api_view(["GET"])
def patient_notifications(request, patient_name):

    notifications = Notification.objects.filter(
        patient=patient_name
    ).order_by("-created_at")

    serializer = NotificationSerializer(
        notifications,
        many=True
    )

    return Response(serializer.data)


@api_view(["POST"])
def create_notification(request):

    notification = Notification.objects.create(

        patient=request.data["patient"],

        title=request.data["title"],

        message=request.data["message"],

        notification_type=request.data.get(
            "notification_type",
            "General"
        )

    )

    serializer = NotificationSerializer(notification)

    return Response(serializer.data)
@api_view(["PUT"])
def mark_all_read(request, patient_name):

    notifications = Notification.objects.filter(
        patient=patient_name,
        is_read=False
    )

    print("Before update:", notifications.count())

    notifications.update(is_read=True)

    after = Notification.objects.filter(
        patient=patient_name,
        is_read=False
    ).count()

    print("After update:", after)

    return Response({
        "message": "All notifications marked as read."
    })
