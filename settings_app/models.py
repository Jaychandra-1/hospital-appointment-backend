from django.db import models

class SystemSettings(models.Model):

    admin_name = models.CharField(max_length=100)

    admin_email = models.EmailField()

    admin_phone = models.CharField(max_length=20)

    appointment_duration = models.IntegerField(default=30)

    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=500
    )

    working_hours = models.CharField(max_length=100)

    emergency_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.admin_name