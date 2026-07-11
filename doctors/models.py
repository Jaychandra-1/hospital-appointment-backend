from django.db import models

class Doctor(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    password = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    qualification = models.CharField(
        max_length=100,
        blank=True
    )

    experience = models.IntegerField(default=0)

    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    hospital = models.CharField(
        max_length=100,
        default="MediConnect Hospital"
    )


    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.FloatField(default=4.5)

    reviews = models.IntegerField(default=0)

    available_days = models.JSONField(default=list)

    slots = models.JSONField(default=list)
    def __str__(self):
        return self.name