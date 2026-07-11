from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    create_order,
    create_appointment,
    patient_appointments,
    doctor_appointments,
    update_appointment_status,
    appointment_history,
    track_appointment,
    admin_dashboard,
    appointments_chart,
    appointment_status_chart
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = router.urls + [

    path(
        "create-order/",
        create_order,
        name="create_order"
    ),

    path(
        "create/",
        create_appointment,
        name="create_appointment"
    ),

    path(
        "patient/<str:patient_name>/",
        patient_appointments,
        name="patient_appointments"
    ),

    path(
        "doctor/<str:doctor_name>/",
        doctor_appointments,
        name="doctor_appointments"
    ),
    path(
    "update-status/<int:appointment_id>/",
    update_appointment_status,
    name="update_appointment_status"
    ),
    path(
    "history/<str:patient_name>/",
    appointment_history,
    name="appointment_history"
),
    path(
    "tracking/<int:appointment_id>/",
    track_appointment,
    name="track_appointment"
),
    path("admin/dashboard/", admin_dashboard),

    path("chart/", appointments_chart),

    path(
    "status-chart/",
    appointment_status_chart,
    name="status-chart"
),
]