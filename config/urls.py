from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
urlpatterns = [

    path("admin/", admin.site.urls),

    # Accounts
    path("api/", include("accounts.urls")),
    path("api/patient/", include("accounts.urls")),

    # Doctors
    path("api/doctors/", include("doctors.urls")),

    # Appointments
    path("api/appointments/", include("appointments.urls")),

    # Payments
    path("api/payments/", include("payments.urls")),

    # Reports
    path("api/reports/", include("reports.urls")),

    # Notifications
    path("api/notifications/", include("notifications.urls")),

    # Reviews
    path("api/reviews/", include("reviews.urls")),

    path("api/leaves/", include("leave.urls")),

    path("api/admin/", include("adminpanel.urls")),

    
]
