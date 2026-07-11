from django.urls import path

from .views import *

urlpatterns=[

    path(
        "admin/profile/",
        admin_profile
    ),

    path(
        "admin/system-settings/",
        system_settings
    ),

]