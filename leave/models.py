from django.db import models
from doctors.models import Doctor


class LeaveRequest(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    FORMAT_CHOICES = (
        ("single", "Single"),
        ("multiple", "Multiple"),
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )

    leave_type = models.CharField(
        max_length=100
    )

    reason = models.TextField()

    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    emergency = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.doctor.name} - {self.start_date} ({self.status})"