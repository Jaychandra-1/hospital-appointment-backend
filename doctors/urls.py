from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DoctorViewSet,
    doctor_login,
    doctor_profile,
)

router = DefaultRouter()
router.register("", DoctorViewSet)

urlpatterns = [

    path("login/", doctor_login, name="doctor_login"),

    path(
        "profile/<int:pk>/",
        doctor_profile,
        name="doctor_profile"
    ),

    path("", include(router.urls)),
]