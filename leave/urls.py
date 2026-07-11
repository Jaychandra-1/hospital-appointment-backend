from django.urls import path
from . import views

urlpatterns = [

    path(
        "create/",
        views.create_leave
    ),

    path(
        "doctor/<int:doctor_id>/",
        views.doctor_leaves
    ),

    path(
        "all/",
        views.all_leave_requests
    ),

    path(
        "approve/<int:leave_id>/",
        views.approve_leave
    ),

    path(
        "reject/<int:leave_id>/",
        views.reject_leave
    ),

]