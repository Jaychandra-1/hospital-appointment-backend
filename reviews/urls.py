from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    DoctorReviewListView,
    DoctorRatingSummaryView,
)

urlpatterns = [
    path("", ReviewListCreateView.as_view(), name="reviews"),
    path("<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
    path("doctor/<str:doctor>/", DoctorReviewListView.as_view(), name="doctor-reviews"),
    path(
    "doctor/<str:doctor>/summary/",
    DoctorRatingSummaryView.as_view(),
    name="doctor-summary"
),
]