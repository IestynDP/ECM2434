from django.urls import path
from apps.qr_scanner.views import qr_scan  # Updated path

urlpatterns = [
    path("scan-qr/", qr_scan, name='qr_scan'),
]