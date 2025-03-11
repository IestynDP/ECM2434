from django.urls import path
from .views import qr_scan

urlpatterns = [
    path("scan-qr/", qr_scan, name='qr_scan'),
]