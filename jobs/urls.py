from django.urls import include, path
from rest_framework import routers

from jobs.views import DoctorViewSet

router = routers.DefaultRouter()
router.register(r"doctor", DoctorViewSet, basename="Doctor")

urlpatterns = [path("", include(router.urls))]
