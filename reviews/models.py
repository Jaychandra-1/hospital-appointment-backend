from django.db import models
from appointments.models import Appointment

class Review(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    patient = models.CharField(max_length=100)

    doctor = models.CharField(max_length=100, blank=True, default="")

    rating = models.IntegerField()

    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"