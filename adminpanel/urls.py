from django.urls import path
from .views import (
    dashboard,
    recent_appointments,
    all_appointments,
    all_doctors
)
urlpatterns = [

    path(
        "dashboard/",
        dashboard
    ),

    path(
        "recent-appointments/",
        recent_appointments
    ),
    path(
        "all-appointments/",
        all_appointments
        ),
    path(
    "all-doctors/",
    all_doctors
),

]