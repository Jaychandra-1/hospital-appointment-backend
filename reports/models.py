from django.db import models
from appointments.models import Appointment

class MedicalReport(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    diagnosis = models.TextField()

    prescription = models.TextField()

    advice = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.appointment.patient.name}"