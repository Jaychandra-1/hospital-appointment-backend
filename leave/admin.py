from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):

    list_display = (
        "doctor",
        "leave_type",
        "start_date",
        "end_date",
        "status",
        "emergency",
    )

    list_filter = (
        "status",
        "emergency",
    )

    search_fields = (
        "doctor__name",
        "leave_type",
    )