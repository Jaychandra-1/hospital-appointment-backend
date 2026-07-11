from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class DoctorReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        doctor = self.kwargs["doctor"]
        return Review.objects.filter(doctor=doctor).order_by("-created_at")
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import Review


class DoctorRatingSummaryView(APIView):

    def get(self, request, doctor):

        reviews = Review.objects.filter(doctor=doctor)

        average = reviews.aggregate(avg=Avg("rating"))["avg"] or 0

        return Response({
            "average_rating": round(average, 1),
            "total_reviews": reviews.count()
        })  