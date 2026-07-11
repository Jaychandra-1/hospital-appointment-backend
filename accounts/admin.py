from django.contrib import admin
from .models import Patient, PasswordResetOTP

admin.site.register(Patient)
admin.site.register(PasswordResetOTP)