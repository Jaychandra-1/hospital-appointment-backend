from django.urls import path

from .views import (
    create_report,
    patient_reports,
    report_detail,
    update_report,
)

urlpatterns = [
    path(
        "create/",
        create_report,
        name="create_report"
    ),

    path(
        "patient/<str:patient_name>/",
        patient_reports,
        name="patient_reports"
    ),
    path(
    "detail/<int:report_id>/",
    report_detail,
    name="report_detail"
),  
    path(
    "update/<int:report_id>/",
    update_report
),
]