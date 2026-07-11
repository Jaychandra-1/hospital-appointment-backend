from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
from django.db import models


class PasswordResetOTP(models.Model):

    email = models.EmailField()

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
