from django.urls import path

from .views import (
    patient_notifications,
    create_notification,
    mark_all_read,
)

urlpatterns = [

    path(
        "patient/<str:patient_name>/",
        patient_notifications,
        name="patient_notifications"
    ),

    path(
        "create/",
        create_notification,
        name="create_notification"
    ),
    path(
    "mark-all-read/<str:patient_name>/",
    mark_all_read,
    name="mark_all_read"
),

]