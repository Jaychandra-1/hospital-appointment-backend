from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    patient_login,
    forgot_password,
    verify_otp,
    reset_password,
    dashboard_counts
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)

urlpatterns = [

    path("login/", patient_login),

    path("forgot-password/", forgot_password),

    path("verify-otp/", verify_otp),

    path("reset-password/", reset_password),

    path("", include(router.urls)),

    path(
    "dashboard/<str:patient_name>/",
    dashboard_counts
    ),
    

]