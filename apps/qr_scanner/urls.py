from django.urls import path
from . import views
from apps.qr_scanner.views import qr_scan  # Updated path

urlpatterns = [
    path('scan/', qr_scan, name='qr_scan'),
]